using System.Net;
using Microsoft.EntityFrameworkCore;
using Tests.Support;

namespace Tests.Controllers.V1;

public class PersonsControllerTests : IntegrationTests
{
    [Fact]
    public async Task ShouldDeletePerson()
    {
        // Arrange
        var dbSet = Context.Set<Person>();
        var salParadise = new Person {Name = "Sal Paradise"};
        dbSet.Add(salParadise);
        await Context.SaveChangesAsync();
        // Act
        var response = await Client.DeleteAsync($"api/v1/Persons/{salParadise.Id}");
        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var person = dbSet.AsNoTracking().FirstOrDefault(x => x.Id == salParadise.Id);
        Assert.Null(person);
    }
}
