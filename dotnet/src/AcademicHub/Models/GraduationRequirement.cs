using System.ComponentModel.DataAnnotations;

namespace AcademicHub.Models;

public class GraduationRequirement
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(50)]
    public string RequirementType { get; set; } = string.Empty;

    [Required]
    public double RequiredCredits { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.Now;
}
