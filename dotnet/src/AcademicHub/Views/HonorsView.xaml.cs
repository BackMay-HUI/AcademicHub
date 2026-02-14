using System.Windows;
using System.Windows.Controls;
using Microsoft.Win32;
using AcademicHub.ViewModels;

namespace AcademicHub.Views;

public partial class HonorsView : UserControl
{
    public HonorsView()
    {
        InitializeComponent();
    }

    private async void ExportCsv_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            Filter = "CSV files (*.csv)|*.csv",
            DefaultExt = "csv",
            FileName = $"honors_{DateTime.Now:yyyyMMdd}"
        };

        if (dialog.ShowDialog() == true)
        {
            var vm = (HonorsViewModel)DataContext;
            await vm.ExportCsv(dialog.FileName);
            MessageBox.Show("导出成功！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }

    private async void ImportCsv_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFileDialog
        {
            Filter = "CSV files (*.csv)|*.csv",
            DefaultExt = "csv"
        };

        if (dialog.ShowDialog() == true)
        {
            var vm = (HonorsViewModel)DataContext;
            var (count, errors) = await vm.ImportCsv(dialog.FileName);

            if (errors.Count > 0)
            {
                MessageBox.Show($"导入完成，但有 {errors.Count} 个错误：\n{string.Join("\n", errors.Take(5))}",
                    "导入结果", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
            else
            {
                MessageBox.Show($"成功导入 {count} 条荣誉记录！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }
}
