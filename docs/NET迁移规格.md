# .NET 迁移规格文档

> 本文档用于记录 AcademicHub 项目的技术规格，为后续迁移到 .NET 平台提供参考。

---

## 1. 项目概述

**项目名称**: AcademicHub - 大学生学业与荣誉管理助手

**核心功能**:
- 成绩管理（含 GPA 计算）
- 荣誉档案
- 毕业追踪
- 保研模拟
- Markdown 笔记
- 简历导出
- 深色/樱花主题模式
- CSV/JSON 数据导入导出
- 图表可视化（成绩分析）

**目标用户**: 大学生

---

## 2. 技术栈对比

### 当前技术栈 (PyQt5)

| 组件 | 技术 |
|------|------|
| 桌面框架 | PyQt5 5.15.x |
| 图表库 | PyQtChart 5.15.7 |
| 数据库 | SQLite3 (内置) |
| 数据格式 | JSON |
| 打包工具 | PyInstaller |

### 建议 .NET 技术栈

| 组件 | 建议技术 | 备选 |
|------|----------|------|
| 桌面框架 | **WPF** | MAUI, Avalonia |
| 图表库 | **LiveCharts2** | OxyPlot, ScottPlot |
| 数据库 | **SQLite** + EF Core | LiteDB |
| MVVM | **CommunityToolkit.Mvvm** | Prism, Caliburn.Micro |
| UI 组件 | **FluentWPF** / MaterialDesign | - |
| 打包 | **MSIX** / 单文件发布 | - |

---

## 3. 数据库结构

> **可直接复用** - SQLite 数据库可迁移到 .NET

### 表: grades (成绩表)

```sql
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,      -- 课程名称
    course_type TEXT NOT NULL,      -- 类型: 必修/选修/限选
    credits REAL NOT NULL,           -- 学分
    score REAL NOT NULL,            -- 成绩分数
    gpa REAL,                        -- 绩点 (可选)
    semester TEXT NOT NULL,         -- 学期: 大一上/大一下/...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 表: honors (荣誉表)

```sql
CREATE TABLE honors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,            -- 荣誉名称
    type TEXT NOT NULL,             -- 类型: 奖学金/竞赛获奖/荣誉称号/社会实践/其他
    level TEXT NOT NULL,            -- 级别: 校级/省级/国家级
    date TEXT NOT NULL,             -- 获得日期
    description TEXT,               -- 描述
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 表: graduation_requirements (毕业要求)

```sql
CREATE TABLE graduation_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requirement_type TEXT NOT NULL, -- 要求类型
    required_credits REAL NOT NULL, -- 所需学分
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 表: notes (笔记表)

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,            -- 笔记标题
    content TEXT,                    -- Markdown 内容
    category TEXT,                   -- 分类
    tags TEXT,                       -- 标签 (逗号分隔)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 表: student_info (学生信息)

```sql
CREATE TABLE student_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,                      -- 姓名
    student_id TEXT,                -- 学号
    major TEXT,                      -- 专业
    grade TEXT,                      -- 年级
    phone TEXT,                      -- 电话
    email TEXT,                      -- 邮箱
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. 功能模块说明

### 4.1 成绩管理 (GradesPage)

**核心功能**:
- 添加/编辑/删除成绩记录
- 按学期筛选
- GPA 统计计算
- CSV 导入/导出
- JSON 全量备份

**UI 组件**:
- 统计卡片: 总学分、总绩点、平均分、课程数
- 表格: 课程名称、类型、学分、成绩、绩点、学期
- 图表页签: 柱状图(学期平均分)、饼图(学分占比)

**业务逻辑**:
- GPA 计算支持标准算法和自定义绩点
- 数据变化时图表自动刷新 (3秒定时)

### 4.2 荣誉档案 (HonorsPage)

**核心功能**:
- 添加/编辑/删除荣誉记录
- 按类型/级别筛选
- 荣誉统计

**UI 组件**:
- 统计卡片: 荣誉总数、各级别数量
- 表格: 荣誉名称、类型、级别、日期、描述
- 列表视图: 荣誉卡片展示

### 4.3 毕业追踪 (GraduationPage)

**核心功能**:
- 设置毕业学分要求
- 追踪已获得学分
- 显示完成进度

**UI 组件**:
- 进度条: 总学分进度
- 类型明细: 各类学分完成情况

### 4.4 保研模拟 (GraduatePage)

**核心功能**:
- 模拟保研成绩计算
- 竞赛加分计算

### 4.5 Markdown 笔记 (NotesPage)

**核心功能**:
- 创建/编辑/删除笔记
- Markdown 实时预览
- 分类和标签

### 4.6 简历导出 (ResumePage)

**核心功能**:
- 自动生成简历
- 导出为文本格式

---

## 5. 主题系统

### 5.1 当前实现 (PyQt5)

```python
# 三套主题: light / dark / sakura
COLORS = {
    "light": {
        "primary": "#1E88E5",
        "background": "#F5F7FA",
        "card": "#FFFFFF",
        "text_primary": "#212121",
        ...
    },
    "dark": {
        "primary": "#64B5F6",
        "background": "#0D1117",
        "card": "#1E1E1E",
        "text_primary": "#FFFFFF",
        ...
    },
    "sakura": {
        "primary": "#FFB7C5",
        "background": "#FFF0F5",
        "card": "#FFFFFF",
        "text_primary": "#5D3A3A",
        ...
    }
}
```

### 5.2 .NET 实现建议

使用 **ResourceDictionary** 分离主题:

```
Themes/
├── LightTheme.xaml
├── DarkTheme.xaml
└── SakuraTheme.xaml
```

```xml
<!-- LightTheme.xaml 示例 -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <SolidColorBrush x:Key="PrimaryBrush" Color="#1E88E5"/>
    <SolidColorBrush x:Key="BackgroundBrush" Color="#F5F7FA"/>
    <SolidColorBrush x:Key="CardBrush" Color="#FFFFFF"/>
    <SolidColorBrush x:Key="TextPrimaryBrush" Color="#212121"/>
</ResourceDictionary>
```

**主题切换**: 动态加载 ResourceDictionary

---

## 6. GPA 计算逻辑

### 6.1 标准算法

```
GPA = Σ(学分 × 绩点) / Σ学分
```

绩点换算 (标准):
| 分数段 | 绩点 |
|--------|------|
| 90-100 | 4.0 |
| 85-89 | 3.7 |
| 82-84 | 3.3 |
| 78-81 | 3.0 |
| 75-77 | 2.7 |
| 72-74 | 2.3 |
| 68-71 | 2.0 |
| 64-67 | 1.3 |
| 60-63 | 1.0 |
| 0-59 | 0 |

### 6.2 自定义算法

用户可自定义绩点映射表，存储于 `data/config.json`:

```json
{
  "gpa_method": "custom",
  "custom_gpa": {
    "100-90": 4.0,
    "89-85": 3.7,
    ...
  }
}
```

### 6.3 .NET 实现建议

```csharp
public class GpaCalculator
{
    public static double CalculateGpa(IEnumerable<Grade> grades, GpaMethod method)
    {
        var points = grades.Select(g => GetPoint(g.Score, method));
        var totalCredits = grades.Sum(g => g.Credits);
        var weightedPoints = grades.Sum(g => g.Credits * GetPoint(g.Score, method));
        return totalCredits > 0 ? weightedPoints / totalCredits : 0;
    }

    private static double GetPoint(double score, GpaMethod method)
    {
        if (method == GpaMethod.Standard)
            return score switch {
                >= 90 => 4.0,
                >= 85 => 3.7,
                >= 82 => 3.3,
                >= 78 => 3.0,
                >= 75 => 2.7,
                >= 72 => 2.3,
                >= 68 => 2.0,
                >= 64 => 1.3,
                >= 60 => 1.0,
                _ => 0
            };
        // 自定义逻辑...
    }
}
```

---

## 7. 配置文件格式

`data/config.json`:

```json
{
  "theme": "sakura",           // light / dark / sakura
  "window": {
    "width": 1880,
    "height": 1400
  },
  "gpa_method": "standard",    // standard / custom
  "custom_gpa": { ... }
}
```

---

## 8. 数据导入/导出

### 8.1 CSV 导入/导出 (成绩)

**导出格式**:
```
课程名称,类型,学分,成绩,绩点,学期
高等数学,必修,4.0,85,3.7,大一上
```

**导入验证**:
- 成绩范围: 0-100
- 学分: > 0
- 学期: 必须在配置列表中

### 8.2 JSON 全量备份

```json
{
  "grades": [...],
  "honors": [...],
  "notes": [...],
  "graduation_requirements": [...],
  "student_info": {...}
}
```

---

## 9. UI 布局结构

```
┌─────────────────────────────────────────────────────────┐
│  NavigationSidebar (侧边导航)                          │
│  ┌──────┐  ┌─────────────────────────────────────────┐  │
│  │ 成绩 │  │  Header (工具栏)                         │  │
│  │ 荣誉 │  │  [GPA设置] [导入] [导出] [添加]          │  │
│  │ 毕业 │  ├─────────────────────────────────────────┤  │
│  │ 保研 │  │                                         │  │
│  │ 笔记 │  │  Content Area                            │  │
│  │ 简历 │  │  (统计卡片 / 表格 / 图表)                │  │
│  │      │  │                                         │  │
│  └──────┘  └─────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 9.1 窗口参数
- 默认大小: 1880 x 1400
- 最小大小: 1400 x 1000
- 侧边导航宽度: ~180px

---

## 10. 迁移检查清单

### 优先级 P0 (核心功能)

- [ ] 数据库迁移 (SQLite)
- [ ] 成绩 CRUD + GPA 计算
- [ ] 荣誉 CRUD
- [ ] 主题切换 (3套主题)
- [ ] 窗口管理 (尺寸/最小化)

### 优先级 P1 (重要功能)

- [ ] 毕业追踪
- [ ] Markdown 笔记
- [ ] CSV 导入/导出
- [ ] JSON 备份/恢复
- [ ] 图表可视化

### 优先级 P2 (增强功能)

- [ ] 保研模拟
- [ ] 简历导出
- [ ] 学生信息管理

### 优先级 P3 (优化)

- [ ] 图表自动刷新
- [ ] 数据验证增强
- [ ] 成绩预警系统

---

## 11. 注意事项

1. **数据库兼容性**: SQLite 文件可直接迁移，无需转换
2. **字体依赖**: 当前使用 `C:/Windows/Fonts/msyh.ttc` (微软雅黑)，.NET 需处理字体回退
3. **图表库选择**: LiveCharts2 与 PyQtChart 功能接近，是较好的替代方案
4. **Markdown 解析**: 可使用 `Markdig` (.NET) 替代 Python 的 `markdown` 库

---

*最后更新: 2026-02-13*
*迁移自: AcademicHub v1.6 (PyQt5)*
