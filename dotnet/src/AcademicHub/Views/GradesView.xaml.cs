using System.Windows;
using System.Windows.Controls;
using Microsoft.Win32;
using AcademicHub.ViewModels;

namespace AcademicHub.Views;

public partial class GradesView : UserControl
{
    public GradesView()
    {
        InitializeComponent();
    }

    private async void ExportCsv_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            Filter = "CSV files (*.csv)|*.csv",
            DefaultExt = ".csv",
            FileName = $"grades_{DateTime.Now:yyyyMMdd}"
        };

        if (dialog.ShowDialog() == true)
        {
            if (DataContext is GradesViewModel vm)
            {
                await vm.ExportCsvCommand.ExecuteAsync(dialog.FileName);
                MessageBox.Show("导出成功！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }

    private async void ImportCsv_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFileDialog
        {
            Filter = "CSV files (*.csv)|*.csv",
            DefaultExt = ".csv"
        };

        if (dialog.ShowDialog() == true)
        {
            if (DataContext is GradesViewModel vm)
            {
                var (count, errors) = await vm.ImportCsv(dialog.FileName);
                if (errors.Count > 0)
                {
                    MessageBox.Show($"导入完成，成功 {count} 条，失败 {errors.Count} 条\n\n{string.Join("\n", errors.Take(5))}",
                        "导入结果", MessageBoxButton.OK, MessageBoxImage.Warning);
                }
                else
                {
                    MessageBox.Show($"成功导入 {count} 条记录！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
        }
    }
}
