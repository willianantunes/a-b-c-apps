using HealthChecks.UI.Client;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Serilog;

var solutionSettings = Path.Combine(Directory.GetCurrentDirectory(), "..", "appsettings.json");
if (!File.Exists(solutionSettings))
    solutionSettings = Path.Combine(Directory.GetCurrentDirectory(), "appsettings.json");

var configuration = new ConfigurationBuilder()
    .AddJsonFile(solutionSettings, optional: false, reloadOnChange: false)
    .AddEnvironmentVariables()
    .Build();

Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(configuration)
    .CreateLogger();

Log.Information("Logger initialized. Starting up the application.");

configuration["ASPNETCORE_URLS"] = configuration["ASPNETCORE_URLS"] is null ? "http://+:8000" : configuration["ASPNETCORE_URLS"];

try
{
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog();
    builder.Configuration.AddConfiguration(configuration);

    // Add services to the container.
    // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen();
    builder.Services.AddHealthChecks();

    var app = builder.Build();

    // Configure the HTTP request pipeline.
    if (app.Environment.IsDevelopment())
    {
        app.UseSwagger();
        app.UseSwaggerUI();
    }

    var summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    app.MapGet("/weatherforecast", () =>
        {
            var forecast = Enumerable.Range(1, 5).Select(index =>
                    new WeatherForecast
                    (
                        DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
                        Random.Shared.Next(-20, 55),
                        summaries[Random.Shared.Next(summaries.Length)]
                    ))
                .ToArray();
            return forecast;
        })
        .WithName("GetWeatherForecast")
        .WithOpenApi();

    app
        .UseHealthChecks("/healthcheck/liveness",
            new HealthCheckOptions
            {
                Predicate = _ => false,
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            })
        .UseHealthChecks("/healthcheck/readiness",
            new HealthCheckOptions
            {
                Predicate = targetHealthCheck => targetHealthCheck.Tags.Contains("crucial"),
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            })
        .UseHealthChecks("/healthcheck/integrations",
            new HealthCheckOptions
            {
                Predicate = targetHealthCheck => targetHealthCheck.Tags.Any(),
                AllowCachingResponses = false,
                ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
            });

    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Host terminated unexpectedly");
}
finally
{
    await Log.CloseAndFlushAsync();
}

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
