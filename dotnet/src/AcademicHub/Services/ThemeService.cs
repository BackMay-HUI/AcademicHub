using System.Windows;

namespace AcademicHub.Services;

public class ThemeService
{
    private static ThemeService? _instance;
    public static ThemeService Instance => _instance ??= new ThemeService();

    private string _currentTheme = "light";

    public string CurrentTheme
    {
        get => _currentTheme;
        set
        {
            if (_currentTheme != value)
            {
                _currentTheme = value;
                ApplyTheme(value);
            }
        }
    }

    public void ApplyTheme(string themeName)
    {
        var app = Application.Current;
        if (app == null) return;

        // Remove existing theme dictionaries
        var toRemove = app.Resources.MergedDictionaries
            .Where(d => d.Source?.ToString().Contains("Theme") == true)
            .ToList();

        foreach (var dict in toRemove)
        {
            app.Resources.MergedDictionaries.Remove(dict);
        }

        // Add new theme
        var themeUri = themeName switch
        {
            "dark" => new Uri("pack://application:,,,/Themes/DarkTheme.xaml"),
            "sakura" => new Uri("pack://application:,,,/Themes/SakuraTheme.xaml"),
            _ => new Uri("pack://application:,,,/Themes/LightTheme.xaml")
        };

        var themeDict = new ResourceDictionary { Source = themeUri };
        app.Resources.MergedDictionaries.Add(themeDict);
    }

    public void Initialize()
    {
        var configService = new ConfigService();
        var theme = configService.GetTheme();
        ApplyTheme(theme);
        _currentTheme = theme;
    }
}
