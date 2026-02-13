using System.IO;
using Newtonsoft.Json;
using AcademicHub.Models;

namespace AcademicHub.Services;

public class ConfigService
{
    private readonly string _configPath;

    public ConfigService()
    {
        // 直接使用固定的相对路径，从 dotnet/src/AcademicHub/bin/Debug/net10.0-windows/ 到项目根目录
        var baseDir = AppDomain.CurrentDomain.BaseDirectory;
        var projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", ".."));
        var dataDir = Path.Combine(projectRoot, "data");

        // 确保数据目录存在
        if (!Directory.Exists(dataDir))
        {
            Directory.CreateDirectory(dataDir);
        }

        _configPath = Path.Combine(dataDir, "config.json");
    }

    public ConfigService(string configPath)
    {
        _configPath = configPath;
    }

    public AppSettings LoadConfig()
    {
        if (File.Exists(_configPath))
        {
            try
            {
                var json = File.ReadAllText(_configPath);
                return JsonConvert.DeserializeObject<AppSettings>(json) ?? new AppSettings();
            }
            catch
            {
                return new AppSettings();
            }
        }
        return new AppSettings();
    }

    public void SaveConfig(AppSettings settings)
    {
        var json = JsonConvert.SerializeObject(settings, Formatting.Indented);
        File.WriteAllText(_configPath, json);
    }

    public void SetTheme(string theme)
    {
        var config = LoadConfig();
        config.Theme = theme;
        SaveConfig(config);
    }

    public string GetTheme()
    {
        return LoadConfig().Theme;
    }

    public void SetGpaMethod(string method, Dictionary<string, double>? customGpa = null)
    {
        var config = LoadConfig();
        config.GpaMethod = method;
        if (customGpa != null)
        {
            config.CustomGpa = customGpa;
        }
        SaveConfig(config);
    }
}
