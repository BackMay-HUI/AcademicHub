using System.Collections.ObjectModel;
using System.IO;
using System.Text;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;

namespace AcademicHub.ViewModels;

public partial class ResumeViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;

    [ObservableProperty]
    private StudentInfo? _studentInfo;

    [ObservableProperty]
    private double _gpa;

    [ObservableProperty]
    private double _totalCredits;

    [ObservableProperty]
    private int _honorCount;

    [ObservableProperty]
    private ObservableCollection<Grade> _recentGrades = new();

    [ObservableProperty]
    private ObservableCollection<Honor> _recentHonors = new();

    [ObservableProperty]
    private string _generatedResume = "";

    public ResumeViewModel()
    {
        _dbService = new DatabaseService();
        _ = LoadDataAsync();
    }

    public async Task LoadDataAsync()
    {
        // Execute all database queries in parallel
        var studentInfoTask = _dbService.GetStudentInfoAsync();
        var gradeStatsTask = _dbService.GetGradeStatsAsync();
        var honorStatsTask = _dbService.GetHonorStatsAsync();
        var gradesTask = _dbService.GetAllGradesAsync();
        var honorsTask = _dbService.GetAllHonorsAsync();

        await Task.WhenAll(studentInfoTask, gradeStatsTask, honorStatsTask, gradesTask, honorsTask);

        StudentInfo = studentInfoTask.Result ?? new StudentInfo();
        var stats = gradeStatsTask.Result;
        Gpa = stats.Gpa;
        TotalCredits = stats.TotalCredits;
        var honorStats = honorStatsTask.Result;
        HonorCount = honorStats.Total;
        RecentGrades = new ObservableCollection<Grade>(gradesTask.Result.Take(10));
        RecentHonors = new ObservableCollection<Honor>(honorsTask.Result.Take(5));

        await GenerateResumeAsync();
    }

    private Task GenerateResumeAsync()
    {
        return Task.Run(() =>
        {
            if (StudentInfo == null)
            {
                GeneratedResume = "请先在设置中填写学生信息";
                return;
            }

            var sb = new StringBuilder();

            sb.AppendLine("===================================");
            sb.AppendLine("           个人简历");
            sb.AppendLine("===================================");
            sb.AppendLine();

            // Basic Info
            sb.AppendLine("【基本信息】");
            sb.AppendLine($"姓名: {StudentInfo.Name ?? "未填写"}");
            sb.AppendLine($"学号: {StudentInfo.StudentId ?? "未填写"}");
            sb.AppendLine($"专业: {StudentInfo.Major ?? "未填写"}");
            sb.AppendLine($"年级: {StudentInfo.Grade ?? "未填写"}");
            sb.AppendLine($"电话: {StudentInfo.Phone ?? "未填写"}");
            sb.AppendLine($"邮箱: {StudentInfo.Email ?? "未填写"}");
            sb.AppendLine();

            // Academic Info
            sb.AppendLine("【学业信息】");
            sb.AppendLine($"总学分: {TotalCredits}");
            sb.AppendLine($"GPA: {Gpa:F2}");
            sb.AppendLine();

            // Honors
            sb.AppendLine("【荣誉奖项】");
            if (RecentHonors.Any())
            {
                foreach (var honor in RecentHonors)
                {
                    sb.AppendLine($"- {honor.Title} ({honor.Level} {honor.Type}) - {honor.Date}");
                    if (!string.IsNullOrEmpty(honor.Description))
                    {
                        sb.AppendLine($"  {honor.Description}");
                    }
                }
            }
            else
            {
                sb.AppendLine("暂无荣誉记录");
            }
            sb.AppendLine();

            // Recent Courses
            sb.AppendLine("【近期课程】");
            if (RecentGrades.Any())
            {
                foreach (var grade in RecentGrades)
                {
                    sb.AppendLine($"- {grade.CourseName} ({grade.CourseType}) - {grade.Credits}学分 - {grade.Score}分");
                }
            }
            else
            {
                sb.AppendLine("暂无成绩记录");
            }

            sb.AppendLine();
            sb.AppendLine("===================================");
            sb.AppendLine($"生成时间: {DateTime.Now:yyyy-MM-dd HH:mm}");

            GeneratedResume = sb.ToString();
        });
    }

    [RelayCommand]
    private async Task SaveStudentInfo()
    {
        if (StudentInfo == null)
        {
            StudentInfo = new StudentInfo();
        }

        await _dbService.SaveStudentInfoAsync(StudentInfo);
        await GenerateResumeAsync();
    }

    [RelayCommand]
    private async Task Refresh()
    {
        await LoadDataAsync();
    }

    [RelayCommand]
    private async Task ExportToFile(string filePath)
    {
        await GenerateResumeAsync();
        await File.WriteAllTextAsync(filePath, GeneratedResume, Encoding.UTF8);
    }

    public async Task ExportToPdf(string filePath)
    {
        try
        {
            PdfExportService.ExportResume(filePath, StudentInfo, Gpa, TotalCredits,
                RecentHonors.ToList(), RecentGrades.ToList());
        }
        catch (Exception ex)
        {
            // Fallback to text if PDF fails
            await GenerateResumeAsync();
            await File.WriteAllTextAsync(filePath.Replace(".pdf", ".txt"), GeneratedResume, Encoding.UTF8);
            throw new Exception($"PDF导出失败，已保存为txt文件: {filePath.Replace(".pdf", ".txt")}");
        }
    }
}
