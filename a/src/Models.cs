using System.ComponentModel.DataAnnotations;

public abstract class StandardEntity
{
    [Key] public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class TodoItem : StandardEntity
{
    public string? Name { get; set; }
    public bool IsComplete { get; set; }
    public User User { get; set; }
    public int UserId { get; set; }
}

public class User : StandardEntity
{
    public IList<TodoItem>? TodoItems { get; set; }
    public string Name { get; set; }
}
