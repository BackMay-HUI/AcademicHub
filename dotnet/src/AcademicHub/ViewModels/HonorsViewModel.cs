using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class HonorsViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;

    [ObservableProperty]
    private ObservableCollection<Honor> _honors = new();

    [ObservableProperty]
    private Honor? _selectedHonor;

    [ObservableProperty]
    private string _selectedType = "全部";

    [ObservableProperty]
    private string _selectedLevel = "全部";

    [ObservableProperty]
    private int _totalHonors;

    [ObservableProperty]
    private int _schoolLevelCount;

    [ObservableProperty]
    private int _provinceLevelCount;

    [ObservableProperty]
    private int _nationalLevelCount;

    [ObservableProperty]
    private bool _isEditing;

    // Form fields
    [ObservableProperty]
    private string _newTitle = "";

    [ObservableProperty]
    private string _newType = "奖学金";

    [ObservableProperty]
    private string _newLevel = "校级";

    [ObservableProperty]
    private string _newDate = DateTime.Now.ToString("yyyy-MM-dd");

    [ObservableProperty]
    private string _newDescription = "";

    public List<string> Types { get; } = new()
    {
        "全部", "奖学金", "竞赛获奖", "荣誉称号", "社会实践", "其他"
    };

    public List<string> Levels { get; } = new() { "全部", "校级", "省级", "国家级" };

    public List<string> HonorTypes { get; } = new()
    {
        "奖学金", "竞赛获奖", "荣誉称号", "社会实践", "其他"
    };

    public List<string> HonorLevels { get; } = new() { "校级", "省级", "国家级" };

    public HonorsViewModel()
    {
        _dbService = new DatabaseService();
        _ = LoadHonorsAsync();
    }

    public async Task LoadHonorsAsync()
    {
        var allHonors = await _dbService.GetAllHonorsAsync();

        if (SelectedType != "全部")
        {
            allHonors = allHonors.Where(h => h.Type == SelectedType).ToList();
        }

        if (SelectedLevel != "全部")
        {
            allHonors = allHonors.Where(h => h.Level == SelectedLevel).ToList();
        }

        Honors = new ObservableCollection<Honor>(allHonors);
        await UpdateStatsAsync();
    }

    private async Task UpdateStatsAsync()
    {
        var stats = await _dbService.GetHonorStatsAsync();
        TotalHonors = stats.Total;
        SchoolLevelCount = stats.ByLevel.GetValueOrDefault("校级", 0);
        ProvinceLevelCount = stats.ByLevel.GetValueOrDefault("省级", 0);
        NationalLevelCount = stats.ByLevel.GetValueOrDefault("国家级", 0);
    }

    partial void OnSelectedTypeChanged(string value)
    {
        _ = LoadHonorsAsync();
    }

    partial void OnSelectedLevelChanged(string value)
    {
        _ = LoadHonorsAsync();
    }

    [RelayCommand]
    private async Task AddHonor()
    {
        if (string.IsNullOrWhiteSpace(NewTitle)) return;

        var honor = new Honor
        {
            Title = NewTitle,
            Type = NewType,
            Level = NewLevel,
            Date = NewDate,
            Description = NewDescription
        };

        await _dbService.AddHonorAsync(honor);
        await LoadHonorsAsync();
        ClearForm();
    }

    [RelayCommand]
    private async Task UpdateHonor()
    {
        if (SelectedHonor == null) return;

        await _dbService.UpdateHonorAsync(SelectedHonor);
        await LoadHonorsAsync();
        IsEditing = false;
    }

    [RelayCommand]
    private async Task DeleteHonor()
    {
        if (SelectedHonor == null) return;

        await _dbService.DeleteHonorAsync(SelectedHonor.Id);
        await LoadHonorsAsync();
        SelectedHonor = null;
    }

    [RelayCommand]
    private void EditHonor()
    {
        if (SelectedHonor == null) return;
        IsEditing = true;
    }

    [RelayCommand]
    private void CancelEdit()
    {
        IsEditing = false;
        _ = LoadHonorsAsync();
    }

    private void ClearForm()
    {
        NewTitle = "";
        NewType = "奖学金";
        NewLevel = "校级";
        NewDate = DateTime.Now.ToString("yyyy-MM-dd");
        NewDescription = "";
    }
}
