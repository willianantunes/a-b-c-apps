using System.Net;
using Microsoft.EntityFrameworkCore;
using Tests.Support;

namespace Tests.Controllers.V1;

public class TodoItemsControllerTests : IntegrationTests
{
    [Fact]
    public async Task ShouldDeleteTodoItem()
    {
        // Arrange
        var dbSet = Context.Set<TodoItem>();
        var jafar = new Person {Name = "Jafar"};
        var learnAspNetCore = new TodoItem {Name = "Learn ASP.NET Core", IsComplete = false, Person = jafar};
        dbSet.Add(learnAspNetCore);
        await Context.SaveChangesAsync();
        // Act
        var response = await Client.DeleteAsync($"api/v1/TodoItems/{learnAspNetCore.Id}");
        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var todoItem = dbSet.AsNoTracking().FirstOrDefault(x => x.Id == learnAspNetCore.Id);
        Assert.Null(todoItem);
    }
}
