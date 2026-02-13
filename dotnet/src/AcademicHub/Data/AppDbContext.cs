using System.IO;
using Microsoft.EntityFrameworkCore;
using AcademicHub.Models;

namespace AcademicHub.Data;

public class AppDbContext : DbContext
{
    public DbSet<Grade> Grades { get; set; } = null!;
    public DbSet<Honor> Honors { get; set; } = null!;
    public DbSet<Note> Notes { get; set; } = null!;
    public DbSet<StudentInfo> StudentInfo { get; set; } = null!;
    public DbSet<GraduationRequirement> GraduationRequirements { get; set; } = null!;

    private readonly string? _dbPath;

    public AppDbContext()
    {
        // 直接使用固定的相对路径，从 dotnet/src/AcademicHub/bin/Debug/net10.0-windows/ 到项目根目录
        var baseDir = AppDomain.CurrentDomain.BaseDirectory;

        // 从 bin/Debug/net10.0-windows/ 向上找4层到项目根目录
        var projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", ".."));
        var dataDir = Path.Combine(projectRoot, "data");

        // 确保数据目录存在
        if (!Directory.Exists(dataDir))
        {
            Directory.CreateDirectory(dataDir);
        }

        _dbPath = Path.Combine(dataDir, "academic.db");
    }

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
        _dbPath = null;
    }

    public AppDbContext(string dbPath)
    {
        _dbPath = dbPath;
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured && _dbPath != null)
        {
            optionsBuilder.UseSqlite($"Data Source={_dbPath}");
        }
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Grade configuration
        modelBuilder.Entity<Grade>(entity =>
        {
            entity.HasIndex(e => e.Semester);
            entity.HasIndex(e => e.CourseType);
        });

        // Honor configuration
        modelBuilder.Entity<Honor>(entity =>
        {
            entity.HasIndex(e => e.Type);
            entity.HasIndex(e => e.Level);
        });

        // Note configuration
        modelBuilder.Entity<Note>(entity =>
        {
            entity.HasIndex(e => e.Category);
        });
    }
}
