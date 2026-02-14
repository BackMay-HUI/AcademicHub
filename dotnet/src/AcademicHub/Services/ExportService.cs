using System.IO;
using System.Text;
using Newtonsoft.Json;
using AcademicHub.Models;

namespace AcademicHub.Services;

public class ExportService
{
    private readonly DatabaseService _dbService;

    public ExportService()
    {
        _dbService = new DatabaseService();
    }

    public ExportService(DatabaseService dbService)
    {
        _dbService = dbService;
    }

    // ===== CSV Export/Import =====
    public async Task ExportGradesToCsvAsync(string filePath)
    {
        var grades = await _dbService.GetAllGradesAsync();
        var sb = new StringBuilder();

        // Header
        sb.AppendLine("课程名称,类型,学分,成绩,绩点,学期");

        // Data
        foreach (var grade in grades)
        {
            sb.AppendLine($"\"{grade.CourseName}\",\"{grade.CourseType}\",{grade.Credits},{grade.Score},{grade.Gpa?.ToString() ?? ""},\"{grade.Semester}\"");
        }

        await File.WriteAllTextAsync(filePath, sb.ToString(), Encoding.UTF8);
    }

    public async Task<(int importedCount, List<string> errors)> ImportGradesFromCsvAsync(string filePath)
    {
        var errors = new List<string>();
        var importedCount = 0;

        var lines = await File.ReadAllLinesAsync(filePath);
        if (lines.Length <= 1) return (0, errors); // No data

        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            try
            {
                var line = lines[i];
                if (string.IsNullOrWhiteSpace(line)) continue;

                // Simple CSV parsing (handles quoted fields)
                var fields = ParseCsvLine(line);
                if (fields.Length < 6) continue;

                var grade = new Grade
                {
                    CourseName = fields[0].Trim(),
                    CourseType = fields[1].Trim(),
                    Credits = double.Parse(fields[2]),
                    Score = double.Parse(fields[3]),
                    Gpa = string.IsNullOrWhiteSpace(fields[4]) ? null : double.Parse(fields[4]),
                    Semester = fields[5].Trim()
                };

                await _dbService.AddGradeAsync(grade);
                importedCount++;
            }
            catch (Exception ex)
            {
                errors.Add($"行 {i + 1}: {ex.Message}");
            }
        }

        return (importedCount, errors);
    }

    private string[] ParseCsvLine(string line)
    {
        var fields = new List<string>();
        var current = new StringBuilder();
        bool inQuotes = false;

        foreach (char c in line)
        {
            if (c == '"')
            {
                inQuotes = !inQuotes;
            }
            else if (c == ',' && !inQuotes)
            {
                fields.Add(current.ToString());
                current.Clear();
            }
            else
            {
                current.Append(c);
            }
        }
        fields.Add(current.ToString());

        return fields.ToArray();
    }

    // ===== Honors CSV Export/Import =====
    public async Task ExportHonorsToCsvAsync(string filePath)
    {
        var honors = await _dbService.GetAllHonorsAsync();
        var sb = new StringBuilder();

        // Header
        sb.AppendLine("荣誉名称,类型,级别,日期,描述");

        // Data
        foreach (var honor in honors)
        {
            sb.AppendLine($"\"{honor.Title}\",\"{honor.Type}\",\"{honor.Level}\",\"{honor.Date}\",\"{honor.Description ?? ""}\"");
        }

        await File.WriteAllTextAsync(filePath, sb.ToString(), Encoding.UTF8);
    }

    public async Task<(int importedCount, List<string> errors)> ImportHonorsFromCsvAsync(string filePath)
    {
        var errors = new List<string>();
        var importedCount = 0;

        var lines = await File.ReadAllLinesAsync(filePath);
        if (lines.Length <= 1) return (0, errors); // No data

        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            try
            {
                var line = lines[i];
                if (string.IsNullOrWhiteSpace(line)) continue;

                // Simple CSV parsing (handles quoted fields)
                var fields = ParseCsvLine(line);
                if (fields.Length < 4) continue;

                var honor = new Honor
                {
                    Title = fields[0].Trim(),
                    Type = fields[1].Trim(),
                    Level = fields[2].Trim(),
                    Date = fields[3].Trim(),
                    Description = fields.Length > 4 ? fields[4].Trim() : ""
                };

                await _dbService.AddHonorAsync(honor);
                importedCount++;
            }
            catch (Exception ex)
            {
                errors.Add($"行 {i + 1}: {ex.Message}");
            }
        }

        return (importedCount, errors);
    }

    // ===== JSON Export/Import =====
    public async Task ExportAllDataAsync(string filePath)
    {
        var data = new
        {
            grades = await _dbService.GetAllGradesAsync(),
            honors = await _dbService.GetAllHonorsAsync(),
            notes = await _dbService.GetAllNotesAsync(),
            graduation_requirements = await _dbService.GetGraduationRequirementsAsync(),
            student_info = await _dbService.GetStudentInfoAsync()
        };

        var json = JsonConvert.SerializeObject(data, Formatting.Indented, new JsonSerializerSettings
        {
            ReferenceLoopHandling = ReferenceLoopHandling.Ignore
        });

        await File.WriteAllTextAsync(filePath, json, Encoding.UTF8);
    }

    public async Task ImportAllDataAsync(string filePath)
    {
        var json = await File.ReadAllTextAsync(filePath);
        var data = JsonConvert.DeserializeObject<dynamic>(json);

        if (data == null) return;

        // Import grades
        if (data.grades != null)
        {
            foreach (var grade in data.grades)
            {
                await _dbService.AddGradeAsync(new Grade
                {
                    CourseName = grade.CourseName,
                    CourseType = grade.CourseType,
                    Credits = grade.Credits,
                    Score = grade.Score,
                    Gpa = grade.Gpa,
                    Semester = grade.Semester
                });
            }
        }

        // Import honors
        if (data.honors != null)
        {
            foreach (var honor in data.honors)
            {
                await _dbService.AddHonorAsync(new Honor
                {
                    Title = honor.Title,
                    Type = honor.Type,
                    Level = honor.Level,
                    Date = honor.Date,
                    Description = honor.Description
                });
            }
        }

        // Import notes
        if (data.notes != null)
        {
            foreach (var note in data.notes)
            {
                await _dbService.AddNoteAsync(new Note
                {
                    Title = note.Title,
                    Content = note.Content,
                    Category = note.Category,
                    Tags = note.Tags
                });
            }
        }

        // Import graduation requirements
        if (data.graduation_requirements != null)
        {
            foreach (var req in data.graduation_requirements)
            {
                await _dbService.SetGraduationRequirementAsync(
                    (string)req.RequirementType,
                    (double)req.RequiredCredits
                );
            }
        }

        // Import student info
        if (data.student_info != null)
        {
            await _dbService.SaveStudentInfoAsync(new StudentInfo
            {
                Name = data.student_info.Name,
                StudentId = data.student_info.StudentId,
                Major = data.student_info.Major,
                Grade = data.student_info.Grade,
                Phone = data.student_info.Phone,
                Email = data.student_info.Email
            });
        }
    }
}
