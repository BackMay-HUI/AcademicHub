using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace AcademicHub;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void MainContent_PreviewMouseWheel(object sender, MouseWheelEventArgs e)
    {
        // Handle mouse wheel scroll for better responsiveness
        var element = sender as DependencyObject;
        if (element != null)
        {
            // Try to find ScrollViewer in visual tree
            var scrollViewer = FindVisualChild<ScrollViewer>(element);
            if (scrollViewer != null)
            {
                // Increase scroll speed for better responsiveness
                double delta = e.Delta > 0 ? -48 : 48;
                scrollViewer.ScrollToVerticalOffset(scrollViewer.VerticalOffset + delta);
                e.Handled = true;
                return;
            }

            // Try to find DataGrid (which has its own scrolling)
            var dataGrid = FindVisualChild<System.Windows.Controls.DataGrid>(element);
            if (dataGrid != null)
            {
                // Scroll DataGrid using its internal ScrollViewer
                var dgScrollViewer = FindVisualChild<ScrollViewer>(dataGrid);
                if (dgScrollViewer != null)
                {
                    double delta = e.Delta > 0 ? -48 : 48;
                    dgScrollViewer.ScrollToVerticalOffset(dgScrollViewer.VerticalOffset + delta);
                    e.Handled = true;
                }
            }
        }
    }

    private static T? FindVisualChild<T>(DependencyObject parent) where T : DependencyObject
    {
        for (int i = 0; i < System.Windows.Media.VisualTreeHelper.GetChildrenCount(parent); i++)
        {
            var child = System.Windows.Media.VisualTreeHelper.GetChild(parent, i);
            if (child is T found)
                return found;

            var result = FindVisualChild<T>(child);
            if (result != null)
                return result;
        }
        return null;
    }
}