using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class MainViewModel : ObservableObject
{
    private readonly ConfigService _configService;

    [ObservableProperty]
    private ObservableObject? _currentView;

    [ObservableProperty]
    private string _currentTheme = "light";

    [ObservableProperty]
    private int _selectedNavIndex = 0;

    // 使用延迟加载
    private GradesViewModel? _gradesViewModel;
    private HonorsViewModel? _honorsViewModel;
    private GraduationViewModel? _graduationViewModel;
    private GraduateViewModel? _graduateViewModel;
    private ResumeViewModel? _resumeViewModel;

    public MainViewModel()
    {
        _configService = new ConfigService();
        CurrentTheme = _configService.GetTheme();

        // 初始只加载成绩页面
        _gradesViewModel = new GradesViewModel();
        CurrentView = _gradesViewModel;

        // 延迟 100ms 加载数据，让窗口先显示出来
        _ = Task.Delay(100).ContinueWith(_ => _gradesViewModel.LoadGradesAsync());
    }

    partial void OnSelectedNavIndexChanged(int value)
    {
        LoadViewForIndex(value);
    }

    private async void LoadViewForIndex(int index)
    {
        try
        {
            switch (index)
            {
                case 0:
                    if (_gradesViewModel == null)
                    {
                        _gradesViewModel = new GradesViewModel();
                        await _gradesViewModel.LoadGradesAsync();
                    }
                    CurrentView = _gradesViewModel;
                    break;
                case 1:
                    if (_honorsViewModel == null)
                    {
                        _honorsViewModel = new HonorsViewModel();
                        await _honorsViewModel.LoadHonorsAsync();
                    }
                    CurrentView = _honorsViewModel;
                    break;
                case 2:
                    if (_graduationViewModel == null)
                    {
                        _graduationViewModel = new GraduationViewModel();
                        await _graduationViewModel.LoadDataAsync();
                    }
                    CurrentView = _graduationViewModel;
                    break;
                case 3:
                    if (_graduateViewModel == null)
                    {
                        _graduateViewModel = new GraduateViewModel();
                        await _graduateViewModel.LoadDataAsync();
                    }
                    CurrentView = _graduateViewModel;
                    break;
                case 4:
                    if (_resumeViewModel == null)
                    {
                        _resumeViewModel = new ResumeViewModel();
                        await _resumeViewModel.LoadDataAsync();
                    }
                    CurrentView = _resumeViewModel;
                    break;
                default:
                    if (_gradesViewModel == null)
                    {
                        _gradesViewModel = new GradesViewModel();
                        await _gradesViewModel.LoadGradesAsync();
                    }
                    CurrentView = _gradesViewModel;
                    break;
            }
        }
        catch
        {
            // 忽略错误，保持当前视图
        }
    }

    [RelayCommand]
    private void ToggleTheme()
    {
        CurrentTheme = CurrentTheme switch
        {
            "light" => "dark",
            "dark" => "sakura",
            "sakura" => "light",
            _ => "light"
        };
        _configService.SetTheme(CurrentTheme);
        ThemeService.Instance.ApplyTheme(CurrentTheme);
    }

    [RelayCommand]
    private async Task RefreshData()
    {
        if (_gradesViewModel != null) await _gradesViewModel.LoadGradesAsync();
        if (_honorsViewModel != null) await _honorsViewModel.LoadHonorsAsync();
        if (_graduationViewModel != null) await _graduationViewModel.LoadDataAsync();
    }
}
