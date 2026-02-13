using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;
using AcademicHub.Models;

namespace AcademicHub.Services;

public static class PdfExportService
{
    static PdfExportService()
    {
        QuestPDF.Settings.License = LicenseType.Community;
    }

    public static void ExportResume(string filePath, StudentInfo? studentInfo, double gpa, double totalCredits,
        List<Honor> honors, List<Grade> grades)
    {
        Document.Create(container =>
        {
            container.Page(page =>
            {
                page.Size(PageSizes.A4);
                page.Margin(40);
                page.DefaultTextStyle(x => x.FontSize(11).FontFamily("Microsoft YaHei"));

                page.Header().Element(c => ComposeHeader(c, studentInfo));
                page.Content().Element(c => ComposeContent(c, studentInfo, gpa, totalCredits, honors, grades));
                page.Footer().AlignCenter().Text(x =>
                {
                    x.Span("第 ");
                    x.CurrentPageNumber();
                    x.Span(" 页，共 ");
                    x.TotalPages();
                    x.Span(" 页");
                });
            });
        }).GeneratePdf(filePath);
    }

    private static void ComposeHeader(IContainer container, StudentInfo? studentInfo)
    {
        container.Row(row =>
        {
            row.RelativeItem().Column(column =>
            {
                column.Item().Text("个人简历")
                    .FontSize(24).Bold().FontColor(Colors.Blue.Medium);

                if (studentInfo != null)
                {
                    column.Item().Text($"{studentInfo.Name ?? "姓名"} | {studentInfo.StudentId ?? "学号"}")
                        .FontSize(12).FontColor(Colors.Grey.Darken1);
                    column.Item().Text($"{studentInfo.Major ?? "专业"} | {studentInfo.Grade ?? "年级"}")
                        .FontSize(12).FontColor(Colors.Grey.Darken1);
                    if (!string.IsNullOrEmpty(studentInfo.Phone) || !string.IsNullOrEmpty(studentInfo.Email))
                    {
                        column.Item().Text($"{studentInfo.Phone ?? ""} | {studentInfo.Email ?? ""}")
                            .FontSize(12).FontColor(Colors.Grey.Darken1);
                    }
                }
            });

            row.ConstantItem(80).Height(80).Background(Colors.Blue.Lighten5)
                .AlignCenter().AlignMiddle().Text("头像").FontSize(10).FontColor(Colors.Grey.Medium);
        });

        container.PaddingBottom(15);
    }

    private static void ComposeContent(IContainer container, StudentInfo? studentInfo, double gpa,
        double totalCredits, List<Honor> honors, List<Grade> grades)
    {
        container.Column(column =>
        {
            // 学业信息
            column.Item().PaddingTop(10).Row(row =>
            {
                row.AutoItem().Text("学业信息").FontSize(14).Bold().FontColor(Colors.Blue.Medium);
            });
            column.Item().PaddingTop(5).LineHorizontal(1).LineColor(Colors.Blue.Lighten2);

            column.Item().PaddingTop(10).Row(row =>
            {
                row.RelativeItem().Text($"总学分: {totalCredits:F1}");
                row.RelativeItem().Text($"GPA: {gpa:F2}");
            });

            // 荣誉奖项
            if (honors.Any())
            {
                column.Item().PaddingTop(20).Row(row =>
                {
                    row.AutoItem().Text("荣誉奖项").FontSize(14).Bold().FontColor(Colors.Blue.Medium);
                });
                column.Item().PaddingTop(5).LineHorizontal(1).LineColor(Colors.Blue.Lighten2);

                column.Item().PaddingTop(10).Column(col =>
                {
                    foreach (var honor in honors.Take(10))
                    {
                        col.Item().PaddingVertical(3).Row(r =>
                        {
                            r.RelativeItem(3).Text($"• {honor.Title}");
                            r.RelativeItem(1).Text($"{honor.Level}");
                            r.RelativeItem(1).Text($"{honor.Date}");
                        });
                    }
                });
            }

            // 课程成绩
            if (grades.Any())
            {
                column.Item().PaddingTop(20).Row(row =>
                {
                    row.AutoItem().Text("课程成绩").FontSize(14).Bold().FontColor(Colors.Blue.Medium);
                });
                column.Item().PaddingTop(5).LineHorizontal(1).LineColor(Colors.Blue.Lighten2);

                column.Item().PaddingTop(10).Column(col =>
                {
                    foreach (var grade in grades.Take(10))
                    {
                        col.Item().PaddingVertical(3).Row(r =>
                        {
                            r.RelativeItem(3).Text($"• {grade.CourseName}");
                            r.RelativeItem(1).Text($"{grade.Credits}学分");
                            r.RelativeItem(1).Text($"{grade.Score}分");
                            r.RelativeItem(1).Text(grade.Gpa.HasValue ? $"{grade.Gpa:F1}" : "");
                        });
                    }
                });
            }
        });
    }
}
