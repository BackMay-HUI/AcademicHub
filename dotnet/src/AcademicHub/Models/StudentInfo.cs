using System.ComponentModel.DataAnnotations;

namespace AcademicHub.Models;

public class StudentInfo
{
    [Key]
    public int Id { get; set; }

    [MaxLength(50)]
    public string? Name { get; set; }

    [MaxLength(30)]
    public string? StudentId { get; set; }

    [MaxLength(50)]
    public string? Major { get; set; }

    [MaxLength(20)]
    public string? Grade { get; set; }

    [MaxLength(20)]
    public string? Phone { get; set; }

    [MaxLength(100)]
    public string? Email { get; set; }

    public DateTime UpdatedAt { get; set; } = DateTime.Now;
}
