using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using AcademicHub.Models;
using AcademicHub.Services;
using Markdig;

namespace AcademicHub.ViewModels;

public partial class NotesViewModel : ObservableObject
{
    private readonly DatabaseService _dbService;
    private readonly MarkdownPipeline _markdownPipeline;

    [ObservableProperty]
    private ObservableCollection<Note> _notes = new();

    [ObservableProperty]
    private Note? _selectedNote;

    [ObservableProperty]
    private string _renderedHtml = "";

    [ObservableProperty]
    private bool _isEditing;

    // Form fields
    [ObservableProperty]
    private string _newTitle = "";

    [ObservableProperty]
    private string _newContent = "";

    [ObservableProperty]
    private string _newCategory = "";

    [ObservableProperty]
    private string _newTags = "";

    public NotesViewModel()
    {
        _dbService = new DatabaseService();
        _markdownPipeline = new MarkdownPipelineBuilder()
            .UseAdvancedExtensions()
            .Build();
        _ = LoadNotesAsync();
    }

    public async Task LoadNotesAsync()
    {
        var allNotes = await _dbService.GetAllNotesAsync();
        Notes = new ObservableCollection<Note>(allNotes);

        if (SelectedNote != null)
        {
            await UpdateRenderedHtmlAsync();
        }
    }

    partial void OnSelectedNoteChanged(Note? value)
    {
        _ = UpdateRenderedHtmlAsync();
    }

    private async Task UpdateRenderedHtmlAsync()
    {
        if (SelectedNote?.Content == null)
        {
            RenderedHtml = "";
            return;
        }

        var html = await Task.Run(() => Markdown.ToHtml(SelectedNote.Content, _markdownPipeline));
        RenderedHtml = WrapInHtmlDocument(html);
    }

    private string WrapInHtmlDocument(string body)
    {
        return $@"<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3 {{ color: #1E88E5; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #1E88E5; margin-left: 0; padding-left: 15px; color: #666; }}
    </style>
</head>
<body>
{body}
</body>
</html>";
    }

    [RelayCommand]
    private async Task AddNote()
    {
        if (string.IsNullOrWhiteSpace(NewTitle)) return;

        var note = new Note
        {
            Title = NewTitle,
            Content = NewContent,
            Category = NewCategory,
            Tags = NewTags
        };

        await _dbService.AddNoteAsync(note);
        await LoadNotesAsync();
        ClearForm();
    }

    [RelayCommand]
    private async Task UpdateNote()
    {
        if (SelectedNote == null) return;

        SelectedNote.Title = NewTitle;
        SelectedNote.Content = NewContent;
        SelectedNote.Category = NewCategory;
        SelectedNote.Tags = NewTags;

        await _dbService.UpdateNoteAsync(SelectedNote);
        await LoadNotesAsync();
        IsEditing = false;
    }

    [RelayCommand]
    private async Task DeleteNote()
    {
        if (SelectedNote == null) return;

        await _dbService.DeleteNoteAsync(SelectedNote.Id);
        SelectedNote = null;
        await LoadNotesAsync();
    }

    [RelayCommand]
    private void EditNote()
    {
        if (SelectedNote == null) return;

        NewTitle = SelectedNote.Title;
        NewContent = SelectedNote.Content ?? "";
        NewCategory = SelectedNote.Category ?? "";
        NewTags = SelectedNote.Tags ?? "";
        IsEditing = true;
    }

    [RelayCommand]
    private void CancelEdit()
    {
        IsEditing = false;
        ClearForm();
    }

    private void ClearForm()
    {
        NewTitle = "";
        NewContent = "";
        NewCategory = "";
        NewTags = "";
    }
}
