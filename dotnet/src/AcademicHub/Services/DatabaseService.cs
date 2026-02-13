using System.IO;
using Microsoft.EntityFrameworkCore;
using AcademicHub.Data;
using AcademicHub.Models;

namespace AcademicHub.Services;

public class DatabaseService
{
    private readonly string _dbPath;

    public DatabaseService()
    {
        // 从 dotnet/src/AcademicHub/bin/Debug/net10.0-windows/ 到项目根目录
        var baseDir = AppDomain.CurrentDomain.BaseDirectory;
        var projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", ".."));
        var dataDir = Path.Combine(projectRoot, "data");

        if (!Directory.Exists(dataDir))
        {
            Directory.CreateDirectory(dataDir);
        }

        _dbPath = Path.Combine(dataDir, "academic.db");
    }

    private AppDbContext CreateContext()
    {
        var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();
        optionsBuilder.UseSqlite($"Data Source={_dbPath}");
        return new AppDbContext(optionsBuilder.Options);
    }

    // ===== Grade =====
    public async Task<List<Grade>> GetAllGradesAsync()
    {
        using var context = CreateContext();
        return await context.Grades
            .OrderByDescending(g => g.Semester)
            .ThenByDescending(g => g.CreatedAt)
            .ToListAsync();
    }

    public async Task<Grade?> GetGradeByIdAsync(int id)
    {
        using var context = CreateContext();
        return await context.Grades.FindAsync(id);
    }

    public async Task<int> AddGradeAsync(Grade grade)
    {
        using var context = CreateContext();
        context.Grades.Add(grade);
        await context.SaveChangesAsync();
        return grade.Id;
    }

    public async Task UpdateGradeAsync(Grade grade)
    {
        using var context = CreateContext();
        context.Grades.Update(grade);
        await context.SaveChangesAsync();
    }

    public async Task DeleteGradeAsync(int id)
    {
        using var context = CreateContext();
        var grade = await context.Grades.FindAsync(id);
        if (grade != null)
        {
            context.Grades.Remove(grade);
            await context.SaveChangesAsync();
        }
    }

    // ===== Honor Operations =====
    public async Task<List<Honor>> GetAllHonorsAsync()
    {
        using var context = CreateContext();
        return await context.Honors
            .OrderByDescending(h => h.Date)
            .ToListAsync();
    }

    public async Task<Honor?> GetHonorByIdAsync(int id)
    {
        using var context = CreateContext();
        return await context.Honors.FindAsync(id);
    }

    public async Task<int> AddHonorAsync(Honor honor)
    {
        using var context = CreateContext();
        context.Honors.Add(honor);
        await context.SaveChangesAsync();
        return honor.Id;
    }

    public async Task UpdateHonorAsync(Honor honor)
    {
        using var context = CreateContext();
        context.Honors.Update(honor);
        await context.SaveChangesAsync();
    }

    public async Task DeleteHonorAsync(int id)
    {
        using var context = CreateContext();
        var honor = await context.Honors.FindAsync(id);
        if (honor != null)
        {
            context.Honors.Remove(honor);
            await context.SaveChangesAsync();
        }
    }

    // ===== Note Operations =====
    public async Task<List<Note>> GetAllNotesAsync()
    {
        using var context = CreateContext();
        return await context.Notes
            .OrderByDescending(n => n.UpdatedAt)
            .ToListAsync();
    }

    public async Task<Note?> GetNoteByIdAsync(int id)
    {
        using var context = CreateContext();
        return await context.Notes.FindAsync(id);
    }

    public async Task<int> AddNoteAsync(Note note)
    {
        using var context = CreateContext();
        context.Notes.Add(note);
        await context.SaveChangesAsync();
        return note.Id;
    }

    public async Task UpdateNoteAsync(Note note)
    {
        using var context = CreateContext();
        note.UpdatedAt = DateTime.Now;
        context.Notes.Update(note);
        await context.SaveChangesAsync();
    }

    public async Task DeleteNoteAsync(int id)
    {
        using var context = CreateContext();
        var note = await context.Notes.FindAsync(id);
        if (note != null)
        {
            context.Notes.Remove(note);
            await context.SaveChangesAsync();
        }
    }

    // ===== Student Info Operations =====
    public async Task<StudentInfo?> GetStudentInfoAsync()
    {
        using var context = CreateContext();
        return await context.StudentInfo.FirstOrDefaultAsync();
    }

    public async Task SaveStudentInfoAsync(StudentInfo studentInfo)
    {
        using var context = CreateContext();
        var existing = await context.StudentInfo.FirstOrDefaultAsync();
        if (existing != null)
        {
            existing.Name = studentInfo.Name;
            existing.StudentId = studentInfo.StudentId;
            existing.Major = studentInfo.Major;
            existing.Grade = studentInfo.Grade;
            existing.Phone = studentInfo.Phone;
            existing.Email = studentInfo.Email;
            existing.UpdatedAt = DateTime.Now;
        }
        else
        {
            context.StudentInfo.Add(studentInfo);
        }
        await context.SaveChangesAsync();
    }

    // ===== Graduation Requirements Operations =====
    public async Task<List<GraduationRequirement>> GetGraduationRequirementsAsync()
    {
        using var context = CreateContext();
        return await context.GraduationRequirements.ToListAsync();
    }

    public async Task SetGraduationRequirementAsync(string requirementType, double requiredCredits)
    {
        using var context = CreateContext();
        var existing = await context.GraduationRequirements
            .FirstOrDefaultAsync(r => r.RequirementType == requirementType);

        if (existing != null)
        {
            existing.RequiredCredits = requiredCredits;
        }
        else
        {
            context.GraduationRequirements.Add(new GraduationRequirement
            {
                RequirementType = requirementType,
                RequiredCredits = requiredCredits
            });
        }
        await context.SaveChangesAsync();
    }

    // ===== Statistics =====
    public async Task<GradeStats> GetGradeStatsAsync()
    {
        using var context = CreateContext();
        var grades = await context.Grades.ToListAsync();

        var totalCredits = grades.Sum(g => g.Credits);
        var creditsByType = grades.GroupBy(g => g.CourseType)
            .ToDictionary(g => g.Key, g => g.Sum(x => x.Credits));

        var gpaCalculator = new GpaCalculator();
        var gpa = gpaCalculator.CalculateGpa(grades);
        var weightedAvg = grades.Sum(g => g.Score * g.Credits) / (totalCredits > 0 ? totalCredits : 1);

        return new GradeStats
        {
            TotalCredits = totalCredits,
            CreditsByType = creditsByType,
            Gpa = Math.Round(gpa, 2),
            WeightedAvg = Math.Round(weightedAvg, 2),
            CourseCount = grades.Count
        };
    }

    public async Task<HonorStats> GetHonorStatsAsync()
    {
        using var context = CreateContext();
        var honors = await context.Honors.ToListAsync();

        var byType = honors.GroupBy(h => h.Type)
            .ToDictionary(g => g.Key, g => g.Count());

        var byLevel = honors.GroupBy(h => h.Level)
            .ToDictionary(g => g.Key, g => g.Count());

        return new HonorStats
        {
            Total = honors.Count,
            ByType = byType,
            ByLevel = byLevel
        };
    }
}

public class GradeStats
{
    public double TotalCredits { get; set; }
    public Dictionary<string, double> CreditsByType { get; set; } = new();
    public double Gpa { get; set; }
    public double WeightedAvg { get; set; }
    public int CourseCount { get; set; }
}

public class HonorStats
{
    public int Total { get; set; }
    public Dictionary<string, int> ByType { get; set; } = new();
    public Dictionary<string, int> ByLevel { get; set; } = new();
}
