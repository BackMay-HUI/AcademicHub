using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AcademicHub.Models;

public class Grade
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string CourseName { get; set; } = string.Empty;

    [Required]
    [MaxLength(20)]
    public string CourseType { get; set; } = string.Empty; // 必修/选修/限选

    [Required]
    public double Credits { get; set; }

    [Required]
    public double Score { get; set; }

    public double? Gpa { get; set; }

    [Required]
    [MaxLength(20)]
    public string Semester { get; set; } = string.Empty; // 大一上/大一下/...

    public DateTime CreatedAt { get; set; } = DateTime.Now;
}
