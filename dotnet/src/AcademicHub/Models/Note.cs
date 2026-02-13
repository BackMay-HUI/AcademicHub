using System.ComponentModel.DataAnnotations;

namespace AcademicHub.Models;

public class Note
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Title { get; set; } = string.Empty;

    public string? Content { get; set; } // Markdown content

    [MaxLength(50)]
    public string? Category { get; set; }

    [MaxLength(200)]
    public string? Tags { get; set; } // Comma-separated tags

    public DateTime CreatedAt { get; set; } = DateTime.Now;

    public DateTime UpdatedAt { get; set; } = DateTime.Now;
}
