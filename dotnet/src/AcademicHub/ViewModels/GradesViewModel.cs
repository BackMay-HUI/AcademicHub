using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class GradesViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;
    private readonly GpaCalculator _gpaCalculator;
    private readonly ExportService _exportService;
    private readonly ConfigService _configService;

    [ObservableProperty]
    private ObservableCollection<Grade> _grades = new();

    [ObservableProperty]
    private Grade? _selectedGrade;

    [ObservableProperty]
    private string _selectedSemester = "全部";

    [ObservableProperty]
    private double _totalCredits;

    [ObservableProperty]
    private double _gpa;

    [ObservableProperty]
    private double _weightedAvg;

    [ObservableProperty]
    private int _courseCount;

    [ObservableProperty]
    private Dictionary<string, double> _creditsByType = new();

    [ObservableProperty]
    private Dictionary<string, double> _gpaBySemester = new();

    [ObservableProperty]
    private Dictionary<string, double> _creditsBySemester = new();

    [ObservableProperty]
    private Dictionary<string, double> _scoresBySemester = new();

    [ObservableProperty]
    private bool _isLoading;

    // Form fields
    [ObservableProperty]
    private string _newCourseName = "";

    [ObservableProperty]
    private string _newCourseType = "必修";

    [ObservableProperty]
    private double? _newCredits;

    [ObservableProperty]
    private double? _newScore;

    [ObservableProperty]
    private string _newSemester = "大一上";

    [ObservableProperty]
    private double? _newGpa;

    [ObservableProperty]
    private bool _isEditing;

    public List<string> Semesters { get; } = new()
    {
        "全部", "大一上", "大一下", "大二上", "大二下", "大三上", "大三下", "大四上", "大四下"
    };

    public List<string> SemesterList { get; } = new()
    {
        "大一上", "大一下", "大二上", "大二下", "大三上", "大三下", "大四上", "大四下"
    };

    public List<string> CourseTypes { get; } = new() { "必修", "选修", "限选" };

    public GradesViewModel()
    {
        _dbService = new DatabaseService();
        _gpaCalculator = new GpaCalculator();
        _exportService = new ExportService();
        _configService = new ConfigService();
    }

    public async Task LoadGradesAsync()
    {
        if (IsLoading) return;

        IsLoading = true;
        try
        {
            var allGrades = await _dbService.GetAllGradesAsync();

            if (SelectedSemester != "全部")
            {
                allGrades = allGrades.Where(g => g.Semester == SelectedSemester).ToList();
            }

            Grades = new ObservableCollection<Grade>(allGrades);
            await UpdateStatsAsync();
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task UpdateStatsAsync()
    {
        var stats = await _dbService.GetGradeStatsAsync();
        TotalCredits = stats.TotalCredits;
        Gpa = stats.Gpa;
        WeightedAvg = stats.WeightedAvg;
        CourseCount = stats.CourseCount;
        CreditsByType = stats.CreditsByType;
    }

    partial void OnSelectedSemesterChanged(string value)
    {
        _ = LoadGradesAsync();
    }

    [RelayCommand]
    private async Task AddGrade()
    {
        if (string.IsNullOrWhiteSpace(NewCourseName)) return;

        var grade = new Grade
        {
            CourseName = NewCourseName,
            CourseType = string.IsNullOrEmpty(NewCourseType) ? "必修" : NewCourseType,
            Credits = NewCredits ?? 0,
            Score = NewScore ?? 0,
            Semester = string.IsNullOrEmpty(NewSemester) ? "大一上" : NewSemester,
            Gpa = NewGpa ?? 0
        };

        await _dbService.AddGradeAsync(grade);
        await LoadGradesAsync();
        ClearForm();
    }

    [RelayCommand]
    private async Task UpdateGrade()
    {
        if (SelectedGrade == null) return;

        await _dbService.UpdateGradeAsync(SelectedGrade);
        await LoadGradesAsync();
        IsEditing = false;
    }

    [RelayCommand]
    private async Task DeleteGrade()
    {
        if (SelectedGrade == null) return;

        await _dbService.DeleteGradeAsync(SelectedGrade.Id);
        await LoadGradesAsync();
        SelectedGrade = null;
    }

    [RelayCommand]
    private void EditGrade()
    {
        if (SelectedGrade == null) return;
        IsEditing = true;
    }

    [RelayCommand]
    private void CancelEdit()
    {
        IsEditing = false;
        _ = LoadGradesAsync();
    }

    [RelayCommand]
    private async Task ExportCsv(string filePath)
    {
        await _exportService.ExportGradesToCsvAsync(filePath);
    }

    [RelayCommand]
    public async Task<(int count, List<string> errors)> ImportCsv(string filePath)
    {
        var (count, errors) = await _exportService.ImportGradesFromCsvAsync(filePath);
        await LoadGradesAsync();
        return (count, errors);
    }

    [RelayCommand]
    private async Task ExportJson(string filePath)
    {
        await _exportService.ExportAllDataAsync(filePath);
    }

    private void ClearForm()
    {
        NewCourseName = "";
        NewCourseType = "必修";
        NewCredits = null;
        NewScore = null;
        NewSemester = "大一上";
        NewGpa = null;
    }
}
