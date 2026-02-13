using System.Configuration;
using System.Data;
using System.Windows;
using AcademicHub.Services;
using AcademicHub.Data;
using Microsoft.EntityFrameworkCore;

namespace AcademicHub;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        ThemeService.Instance.Initialize();
        InitializeDatabase();
    }

    private void InitializeDatabase()
    {
        try
        {
            using var context = new AppDbContext();
            context.Database.EnsureCreated();
        }
        catch
        {
            // 忽略数据库初始化错误
        }
    }
}

