# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本项目中工作时提供指导。

## 项目概述

**AcademicHub** 是一款面向大学生的 WPF 桌面应用，用于管理学业成绩、荣誉档案、毕业追踪、保研模拟、Markdown 笔记和简历导出。

## 构建与运行命令

```bash
# 运行源码（需要 .NET 10.0 SDK）
cd dotnet/src/AcademicHub
dotnet run

# 构建发布版本（单文件发布）
cd dotnet/src/AcademicHub
dotnet publish -c Release

# 发布的 exe 位于: dotnet/src/AcademicHub/bin/Release/net10.0-windows/win-x64/publish/AcademicHub.exe
```

## 架构

应用采用 **MVVM 模式**，使用 CommunityToolkit.Mvvm 实现。

### 核心组件

- **Models** (`dotnet/src/AcademicHub/Models/`): 数据实体 (Grade, Honor, Note, StudentInfo, GraduationRequirement)
- **ViewModels** (`dotnet/src/AcademicHub/ViewModels/`): 业务逻辑，使用 ObservableObject 和 RelayCommand
- **Views** (`dotnet/src/AcademicHub/Views/`): XAML 页面视图
- **Services** (`dotnet/src/AcademicHub/Services/`):
  - `DatabaseService.cs` - EF Core 数据库操作
  - `GpaCalculator.cs` - GPA 计算逻辑
  - `ThemeService.cs` - 主题切换 (light/dark/sakura)
  - `ConfigService.cs` - 用户配置存储
  - `ExportService.cs` / `PdfExportService.cs` - 数据导出
- **Data** (`dotnet/src/AcademicHub/Data/AppDbContext.cs`): EF Core DbContext，连接 SQLite

### 导航

MainViewModel 通过 `SelectedNavIndex` 属性控制标签页导航 (0-4):
- 0: GradesView（成绩管理）
- 1: HonorsView（荣誉档案）
- 2: GraduationView（毕业追踪）
- 3: GraduateView（保研模拟）
- 4: ResumeView（简历导出）

视图采用延迟加载，首次访问对应标签页时才会实例化。

### 数据存储

- 数据库: `data/academic.db` (SQLite)
- 配置: `data/config.json`
- 路径相对于项目根目录，而非可执行文件

### 主题

三种主题位于 `dotnet/src/AcademicHub/Themes/`:
- LightTheme.xaml（浅色）
- DarkTheme.xaml（深色）
- SakuraTheme.xaml（樱花）

运行时通过 ThemeService 动态应用主题。

## 关键模式

1. **每操作一个 Context**: DatabaseService 为每个异步操作创建新的 DbContext（使用 using 语句）
2. **Observable 属性**: 使用 CommunityToolkit.Mvvm 的 `[ObservableProperty]` 和 `[ObservableProperty]` 特性
3. **RelayCommand**: 使用 `[RelayCommand]` 特性处理按钮绑定
4. **延迟加载**: ViewModels 仅在首次访问对应标签页时才会被实例化

## 自定义指令

用户可使用以下便捷指令：

### ./bootnet

运行项目，等同于：
```bash
cd E:/Project/Scores_management_system/dotnet/src/AcademicHub && dotnet run
```

### ./upreadme

执行以下操作：
1. 更新开发日志 (docs/开发日志.md)，添加今天的更新内容
2. 更新 README.md（如有必要）
3. 将整个项目同步更新到 GitHub（git add -> git commit -> git push）

使用示例：
```
./upreadme 添加了荣誉档案的CSV导入导出功能
```
（后面的文字将作为提交信息）
