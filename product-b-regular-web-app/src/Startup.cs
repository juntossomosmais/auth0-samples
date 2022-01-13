using System;
using Auth0.AspNetCore.Authentication;
using IdentityModel.OidcClient;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using ProductBee.Support;

namespace ProductBee
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {
            // https://github.com/IdentityModel/IdentityModel.OidcClient
            // https://identitymodel.readthedocs.io/en/latest/native/manual.html
            services.AddSingleton(new OidcClientOptions
            {
                Authority = $"https://{Configuration["Auth0:Domain"]}",
                ClientId = Configuration["Auth0:ClientId"],
                ClientSecret = Configuration["Auth0:ClientSecret"],
                // Hard-coded, yes, but for testing purpose!
                RedirectUri = "http://app.local:8001/Account/Callback", 
                Scope = Configuration["Auth0:Scope"],
            });
            // Session configuration. Look at AccountController and know more why this is required!
            // This is for testing purpose only, not for a production environment.
            // https://docs.microsoft.com/en-us/aspnet/core/fundamentals/app-state?view=aspnetcore-5.0
            services.AddDistributedMemoryCache();
            // services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme);
            services.AddSession(options =>
            {
                options.Cookie.Name = ".ProductB.Session";
                options.IdleTimeout = TimeSpan.FromSeconds(120);
                options.Cookie.HttpOnly = false;
                options.Cookie.IsEssential = true;
            });
            // https://docs.microsoft.com/en-us/aspnet/core/security/authentication/cookie?view=aspnetcore-5.0#configuration
            services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme).AddCookie(options =>
            {
                options.Cookie.Name = ".ProductB.Authentication";
            });
            // https://stackoverflow.com/questions/62251347/services-addcontrollerswithviews-vs-services-addmvc#comment112694342_62251652
            services.AddControllersWithViews();
            // https://stackoverflow.com/a/58300981/3899136
            services
                .AddControllersWithViews()
                .AddRazorRuntimeCompilation();
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Home/Error");
            }

            app.UseStaticFiles();

            app.UseRouting();
            
            // These three added by me :)
            app.UseAuthentication();
            app.UseAuthorization();
            app.UseSession();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllerRoute(
                    name: "default",
                    pattern: "{controller=Home}/{action=Index}/{id?}");
            });
        }
    }
}