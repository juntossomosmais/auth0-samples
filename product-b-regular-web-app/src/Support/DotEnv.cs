using System;
using System.IO;
using System.Linq;

namespace ProductBee.Support
{
    public static class DotEnv
    {
        public static DirectoryInfo TryGetSolutionDirectoryInfo(string? currentPath = null)
        {
            var directory = new DirectoryInfo(currentPath ?? Directory.GetCurrentDirectory());

            while (directory != null && !directory.GetFiles("*.sln").Any())
            {
                directory = directory.Parent;
            }

            return directory!;
        }

        public static void Load(string envFileName)
        {
            var whereSolutionFileIs = TryGetSolutionDirectoryInfo();
            var filePath = Path.Combine(whereSolutionFileIs.FullName, ".env.development");

            if (!File.Exists(filePath)) return;

            foreach (var line in File.ReadAllLines(filePath))
            {
                var isLineSomeCommentOrEmpty = line.StartsWith("#") is not false || line == "";
                if (isLineSomeCommentOrEmpty) continue;

                var parts = line.Split('=', StringSplitOptions.RemoveEmptyEntries);
                var isArrayInvalidToSetEnvironmentVariable = parts.Length != 2;
                if (isArrayInvalidToSetEnvironmentVariable) throw new InvalidOperationException();

                Environment.SetEnvironmentVariable(parts[0], parts[1]);
            }
        }
    }
}