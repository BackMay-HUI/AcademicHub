using System.Windows;
using System.Windows.Controls;
using Microsoft.Win32;
using AcademicHub.ViewModels;

namespace AcademicHub.Views;

public partial class ResumeView : UserControl
{
    public ResumeView()
    {
        InitializeComponent();
    }

    private async void ExportResume_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            Filter = "Text files (*.txt)|*.txt",
            DefaultExt = ".txt",
            FileName = $"resume_{DateTime.Now:yyyyMMdd}"
        };

        if (dialog.ShowDialog() == true)
        {
            if (DataContext is ResumeViewModel vm)
            {
                await vm.ExportToFileCommand.ExecuteAsync(dialog.FileName);
                MessageBox.Show("导出成功！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }
}
