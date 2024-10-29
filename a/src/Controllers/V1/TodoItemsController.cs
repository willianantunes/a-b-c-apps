using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NDjango.RestFramework.Base;
using NDjango.RestFramework.Filters;
using NDjango.RestFramework.Serializer;

namespace LetterA.Controllers.V1;

public class TodoItemDto : BaseDto<int>
{
    public string Name { get; set; }
    public bool IsComplete { get; set; }
    public int UserId { get; set; }
}

public class TodoItemIncludePersonFilter : Filter<TodoItem>
{
    public override IQueryable<TodoItem> AddFilter(IQueryable<TodoItem> query, HttpRequest request)
    {
        return query.Include(navigationPropertyPath => navigationPropertyPath.Person);
    }
}

[ApiController]
[Route("api/v1/[controller]")]
public class TodoItemsController : BaseController<TodoItemDto, TodoItem, int, AppDbContext>
{
    public TodoItemsController(
        Serializer<TodoItemDto, TodoItem, int, AppDbContext> serializer,
        AppDbContext context,
        ILogger<TodoItem> logger
    ) : base(serializer, context, logger)
    {
        AllowedFields =
        [
            nameof(TodoItem.UserId),
            nameof(TodoItem.Name),  
            nameof(TodoItem.IsComplete),
            nameof(TodoItem.CreatedAt),
            nameof(TodoItem.UpdatedAt)
        ];

        Filters.Add(new QueryStringFilter<TodoItem>(AllowedFields));
        Filters.Add(new QueryStringIdRangeFilter<TodoItem, int>());
        Filters.Add(new TodoItemIncludePersonFilter());
    }
}
