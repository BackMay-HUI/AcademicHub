using AcademicHub.Models;

namespace AcademicHub.Services;

public class GpaCalculator
{
    private readonly ConfigService _configService;

    public GpaCalculator()
    {
        _configService = new ConfigService();
    }

    public double CalculateGpa(IEnumerable<Grade> grades)
    {
        var settings = _configService.LoadConfig();
        var method = settings.GpaMethod;

        var gradeList = grades.ToList();
        if (!gradeList.Any()) return 0;

        var totalCredits = gradeList.Sum(g => g.Credits);
        if (totalCredits <= 0) return 0;

        double totalGradePoints = 0;
        foreach (var grade in gradeList)
        {
            var gpa = grade.Gpa ?? GetPoint(grade.Score, method, settings.CustomGpa);
            totalGradePoints += gpa * grade.Credits;
        }

        return totalGradePoints / totalCredits;
    }

    public double GetPoint(double score, string method, Dictionary<string, double>? customGpa = null)
    {
        if (method == "custom" && customGpa != null)
        {
            return GetCustomPoint(score, customGpa);
        }
        return GetStandardPoint(score);
    }

    private double GetStandardPoint(double score)
    {
        return score switch
        {
            >= 90 => 4.0,
            >= 85 => 3.7,
            >= 82 => 3.3,
            >= 78 => 3.0,
            >= 75 => 2.7,
            >= 72 => 2.3,
            >= 68 => 2.0,
            >= 64 => 1.3,
            >= 60 => 1.0,
            _ => 0.0
        };
    }

    private double GetCustomPoint(double score, Dictionary<string, double> customGpa)
    {
        foreach (var kvp in customGpa)
        {
            var parts = kvp.Key.Split('-');
            if (parts.Length == 2)
            {
                if (int.TryParse(parts[0], out int maxScore) && int.TryParse(parts[1], out int minScore))
                {
                    if (minScore <= score && score <= maxScore)
                    {
                        return kvp.Value;
                    }
                }
            }
        }
        return 0;
    }

    public static List<string> GetStandardGpaRanges()
    {
        return new List<string>
        {
            "90-100: 4.0",
            "85-89: 3.7",
            "82-84: 3.3",
            "78-81: 3.0",
            "75-77: 2.7",
            "72-74: 2.3",
            "68-71: 2.0",
            "64-67: 1.3",
            "60-63: 1.0",
            "0-59: 0"
        };
    }
}
