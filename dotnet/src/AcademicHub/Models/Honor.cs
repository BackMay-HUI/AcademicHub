using System.ComponentModel.DataAnnotations;

namespace AcademicHub.Models;

public class Honor
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Title { get; set; } = string.Empty;

    [Required]
    [MaxLength(20)]
    public string Type { get; set; } = string.Empty; // 奖学金/竞赛获奖/荣誉称号/社会实践/其他

    [Required]
    [MaxLength(20)]
    public string Level { get; set; } = string.Empty; // 校级/省级/国家级

    [Required]
    [MaxLength(20)]
    public string Date { get; set; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.Now;
}
