using NDjango.RestFramework.Base;

public abstract class StandardEntity : BaseModel<int>
{
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class TodoItem : StandardEntity
{
    public string? Name { get; set; }
    public bool IsComplete { get; set; }
    public Person Person { get; set; }
    public int UserId { get; set; }

    public override string[] GetFields()
    {
        return
        [
            "Id",
            "Name",
            "IsComplete",
            "CreatedAt",
            "UpdatedAt",
            "UserId",
            "Person",
            "Person:Name",
        ];
    }
}

public class Person : StandardEntity
{
    public IList<TodoItem>? TodoItems { get; set; }
    public string Name { get; set; }
    public override string[] GetFields()
    {
        return
        [
            "Id",
            "Name",
            "CreatedAt",
            "UpdatedAt"
        ];
    }
}
