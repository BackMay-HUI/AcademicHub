using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class GraduationViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;

    [ObservableProperty]
    private ObservableCollection<GraduationRequirement> _requirements = new();

    [ObservableProperty]
    private double _totalRequiredCredits;

    [ObservableProperty]
    private double _totalEarnedCredits;

    [ObservableProperty]
    private double _completionPercentage;

    [ObservableProperty]
    private Dictionary<string, double> _creditsByType = new();

    [ObservableProperty]
    private Dictionary<string, double> _requiredByType = new();

    // Form fields
    [ObservableProperty]
    private string _newRequirementType = "必修";

    [ObservableProperty]
    private double _newRequiredCredits = 30;

    public List<string> RequirementTypes { get; } = new()
    {
        "必修", "选修", "限选", "公选", "实践"
    };

    public GraduationViewModel()
    {
        _dbService = new DatabaseService();
        _ = LoadDataAsync();
    }

    public async Task LoadDataAsync()
    {
        var requirements = await _dbService.GetGraduationRequirementsAsync();
        Requirements = new ObservableCollection<GraduationRequirement>(requirements);

        var stats = await _dbService.GetGradeStatsAsync();

        TotalRequiredCredits = requirements.Sum(r => r.RequiredCredits);
        TotalEarnedCredits = stats.TotalCredits;
        CreditsByType = stats.CreditsByType;

        // Calculate required by type
        RequiredByType = requirements.ToDictionary(r => r.RequirementType, r => r.RequiredCredits);

        // Calculate completion percentage
        CompletionPercentage = TotalRequiredCredits > 0
            ? Math.Round((TotalEarnedCredits / TotalRequiredCredits) * 100, 1)
            : 0;
    }

    [RelayCommand]
    private async Task AddRequirement()
    {
        if (NewRequiredCredits <= 0) return;

        await _dbService.SetGraduationRequirementAsync(NewRequirementType, NewRequiredCredits);
        await LoadDataAsync();
    }

    [RelayCommand]
    private async Task UpdateRequirement(GraduationRequirement req)
    {
        await _dbService.SetGraduationRequirementAsync(req.RequirementType, req.RequiredCredits);
        await LoadDataAsync();
    }

    public double GetCompletedCredits(string type)
    {
        return CreditsByType.GetValueOrDefault(type, 0);
    }

    public double GetRequiredCredits(string type)
    {
        return RequiredByType.GetValueOrDefault(type, 0);
    }

    public double GetTypeCompletionPercentage(string type)
    {
        var required = GetRequiredCredits(type);
        if (required <= 0) return 0;
        return Math.Min(100, (GetCompletedCredits(type) / required) * 100);
    }
}
