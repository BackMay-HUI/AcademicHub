using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class GraduateViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;

    [ObservableProperty]
    private double _gpaScore;

    [ObservableProperty]
    private double _honorBonus;

    [ObservableProperty]
    private double _totalScore;

    [ObservableProperty]
    private ObservableCollection<Honor> _competitionHonors = new();

    [ObservableProperty]
    private StudentInfo? _studentInfo;

    // Honor bonus settings
    [ObservableProperty]
    private int _nationalFirstCount;

    [ObservableProperty]
    private int _nationalSecondCount;

    [ObservableProperty]
    private int _provinceFirstCount;

    [ObservableProperty]
    private int _provinceSecondCount;

    [ObservableProperty]
    private int _schoolLevelCount;

    public GraduateViewModel()
    {
        _dbService = new DatabaseService();
        _ = LoadDataAsync();
    }

    public async Task LoadDataAsync()
    {
        var stats = await _dbService.GetGradeStatsAsync();
        GpaScore = stats.Gpa * 25; // Convert GPA to 100-point scale

        var honors = await _dbService.GetAllHonorsAsync();
        CompetitionHonors = new ObservableCollection<Honor>(
            honors.Where(h => h.Type == "竞赛获奖" || h.Type == "奖学金")
        );

        StudentInfo = await _dbService.GetStudentInfoAsync();

        // Calculate honor bonus
        NationalFirstCount = honors.Count(h => h.Level == "国家级" && h.Type == "竞赛获奖");
        NationalSecondCount = honors.Count(h => h.Level == "国家级" && h.Type == "奖学金");
        ProvinceFirstCount = honors.Count(h => h.Level == "省级" && h.Type == "竞赛获奖");
        ProvinceSecondCount = honors.Count(h => h.Level == "省级" && h.Type == "奖学金");
        SchoolLevelCount = honors.Count(h => h.Level == "校级");

        // Calculate bonus (simplified algorithm)
        HonorBonus = NationalFirstCount * 10 + NationalSecondCount * 7 +
                     ProvinceFirstCount * 5 + ProvinceSecondCount * 3 +
                     SchoolLevelCount * 1;

        TotalScore = GpaScore + HonorBonus;
    }

    [RelayCommand]
    private async Task Recalculate()
    {
        await LoadDataAsync();
    }

    public string GetRecommendation()
    {
        if (TotalScore >= 90) return "很有机会获得保研资格";
        if (TotalScore >= 80) return "有机会获得保研资格";
        if (TotalScore >= 70) return "需要继续努力";
        return "建议通过考研等其他途径";
    }
}
