using System;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using System.Web;
using IdentityModel.OidcClient;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.Extensions;
using Microsoft.AspNetCore.Mvc;
using ProductBee.Models;
using ProductBee.Support;

namespace ProductBee.Controllers
{
    public class AccountController : Controller
    {
        private readonly OidcClientOptions _oidcClientOptions;
        private readonly string _sessionKey;

        public AccountController(OidcClientOptions oidcClientOptions)
        {
            _oidcClientOptions = oidcClientOptions;
            _sessionKey = "auth-code";
        }

        public async Task<RedirectResult> Login()
        {
            var client = new OidcClient(_oidcClientOptions);
            var state = await client.PrepareLoginAsync();
            // Keeping track of the state so we can retrieve it later
            HttpContext.Session.Set<AuthorizeState>(_sessionKey, state);

            return Redirect(state.StartUrl);
        }

        public async Task<RedirectToActionResult> Callback()
        {
            var client = new OidcClient(_oidcClientOptions);
            var createdStateWhenTheFlowWasInitiated = HttpContext.Session.Get<AuthorizeState>(_sessionKey);
            var urlToBeParsed = Request.GetDisplayUrl();
            var result = await client.ProcessResponseAsync(urlToBeParsed, createdStateWhenTheFlowWasInitiated);
            // Sign in a principal for the default authentication scheme.
            await HttpContext.SignInAsync(result.User);

            return RedirectToAction(controllerName: "Home", actionName: "Index");
        }

        [Authorize]
        public async Task<RedirectResult> Logout()
        {
            var logoutUrl = $"{_oidcClientOptions.Authority}/v2/logout";
            var uriBuilder = new UriBuilder(logoutUrl);
            var query = HttpUtility.ParseQueryString(uriBuilder.Query);
            query["returnTo"] = Url.ActionLink("Index", "Home");
            query["client_id"] = _oidcClientOptions.ClientId;
            uriBuilder.Query = query.ToString();
            var logoutUri = uriBuilder.Uri.AbsoluteUri;

            // Clear current session
            HttpContext.Session.Clear();
            // Delete temporary cookie used during external authentication
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            // Clear session on Auth0
            return Redirect(logoutUri);
        }

        [Authorize]
        public async Task<IActionResult> Profile()
        {
            // https://docs.identityserver.io/en/latest/quickstarts/3_aspnetcore_and_apis.html#using-the-access-token
            var accessToken = await HttpContext.GetTokenAsync("access_token");
            var idToken = await HttpContext.GetTokenAsync("id_token");
            var refreshToken = await HttpContext.GetTokenAsync("refresh_token");

            return View(new UserProfileViewModel()
            {
                Id = User.Claims.FirstOrDefault(c => c.Type == "sub")?.Value,
                Name = User.Identity.Name,
                EmailAddress = User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.Email)?.Value,
                ProfileImage = User.Claims.FirstOrDefault(c => c.Type == "picture")?.Value
            });
        }

        [Authorize]
        public IActionResult Claims()
        {
            return View();
        }

        public IActionResult AccessDenied()
        {
            return View();
        }
    }
}