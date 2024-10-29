using System.Text.Json;
using lnn_ui.Models;

namespace lnn_ui.Services;

public class HistoryService
{
    private readonly HttpClient _client;
    private readonly IConfiguration _config;
    private readonly ILogger<HistoryService> _logger;

    public HistoryService(HttpClient client, IConfiguration config, ILogger<HistoryService> logger)
    {
        _client = client;
        _config = config;
        _logger = logger;
    }

    public async Task<List<LnnOutput>> GetHistory(int count)
    {
        try
        {
            var apiUrl = _config.GetConnectionString("ApiUrl");
            _logger.LogInformation($"Attempting to fetch history from: {apiUrl}/get-history?count={count}");

            // Important: await the GetAsync call immediately
            var response = await _client.GetAsync($"{apiUrl}/get-history?count={count}");
            
            // Log the response status code
            _logger.LogInformation($"API Response Status: {response.StatusCode}");

            if (!response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                _logger.LogError($"API returned error: {response.StatusCode}, Content: {content}");
                return [];
            }

            var jsonContent = await response.Content.ReadAsStringAsync();
            _logger.LogInformation($"Received JSON: {jsonContent}");

            return JsonSerializer.Deserialize<List<LnnOutput>>(jsonContent) ?? [];
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError($"HTTP Request failed: {ex.Message}");
            return [];
        }
        catch (JsonException ex)
        {
            _logger.LogError($"JSON Deserialization failed: {ex.Message}");
            return [];
        }
        catch (Exception ex)
        {
            _logger.LogError($"Unexpected error: {ex.Message}");
            return [];
        }
    }
}