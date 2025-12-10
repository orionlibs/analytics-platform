const OpenAI = require('openai');
const { expect } = require('chai');

describe('chat_v1 Tests', () => {
  let openai;
  let monitor_v1;

  before(async () => {
    // Initialize OpenAI client
    openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    const monitoringOptions = {
      metrics_url: process.env.METRICS_URL,
      logs_url: process.env.LOGS_URL,
      metrics_username: process.env.METRICS_USERNAME,
      logs_username: process.env.LOGS_USERNAME,
      access_token: process.env.ACCESS_TOKEN,
    };

    // Use dynamic import to import the ES module and call the function
    const module = await import('../src/chat_v1.js');
    monitor_v1 = module.default; // Assuming 'createMonitor_v1' is the default export
    monitor_v1(openai, monitoringOptions);
  });

  it('should return a response with object as "text_completion"', async () => {
    const completion = await openai.completions.create({
      model: 'gpt-3.5-turbo-instruct',
      prompt: 'Say this is a test.',
      max_tokens: 7,
      temperature: 0,
    });

    // Assertion: Check if response.object is 'text_completion'
    expect(completion.object).to.equal('text_completion');
  });

  // Add more test cases as needed

  after(() => {
    // Clean up or perform any necessary teardown
  });
});
