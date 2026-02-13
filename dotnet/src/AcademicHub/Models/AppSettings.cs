namespace AcademicHub.Models;

public class AppSettings
{
    public string Theme { get; set; } = "light";
    public WindowSettings Window { get; set; } = new();
    public string GpaMethod { get; set; } = "standard";
    public Dictionary<string, double> CustomGpa { get; set; } = new()
    {
        { "100-90", 4.0 },
        { "89-85", 3.7 },
        { "84-82", 3.3 },
        { "81-78", 3.0 },
        { "77-75", 2.7 },
        { "74-72", 2.3 },
        { "71-68", 2.0 },
        { "67-64", 1.3 },
        { "63-60", 1.0 },
        { "59-0", 0 }
    };
}

public class WindowSettings
{
    public int Width { get; set; } = 1880;
    public int Height { get; set; } = 1400;
}
