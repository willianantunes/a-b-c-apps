using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace Tests.Support;

public class IntegrationTests
{
    protected readonly HttpClient Client;
    protected readonly AppDbContext Context;

    protected IntegrationTests()
    {
        var oldDbValue = "Initial Catalog=LetterA";
        var newDbValue = $"Initial Catalog=test_{Guid.NewGuid()}";
        var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                string? newConnectionString = null;
                builder.ConfigureAppConfiguration((context, _) =>
                {
                    var configuration = context.Configuration;
                    var connectionString = configuration.GetConnectionString("AppDbContext");
                    newConnectionString = connectionString.Replace(oldDbValue, newDbValue);
                }).ConfigureTestServices(services =>
                {
                    services.RemoveAll<AppDbContext>();
                    services.RemoveAll<DbContextOptions<AppDbContext>>();
                    services.AddDbContext<AppDbContext>(options => { options.UseSqlServer(newConnectionString); },
                        ServiceLifetime.Singleton);
                });
            });
        Client = factory.CreateClient();
        Context = factory.Services.GetRequiredService<AppDbContext>();
    }
}
