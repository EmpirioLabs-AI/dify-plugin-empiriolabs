# EmpirioLabs AI

[EmpirioLabs AI](https://empiriolabs.ai/) is a specialized AI inference and integration provider. It hosts open-source models on GPU infrastructure it manages, runs optimized endpoints for proprietary models, helps teams ship their own models, and offers on-demand GPU Cloud instances and hosted AI agents. Its model catalog spans text, image, audio, video, transcription, embedding, reranking, research, and 3D models.

This plugin lets Dify use EmpirioLabs AI as a model provider for LLM nodes, agents, and workflows. It sends requests to the EmpirioLabs AI API:

```text
https://api.empiriolabs.ai/v1
```

## Configure

1. Create an EmpirioLabs AI account and an [API key](https://platform.empiriolabs.ai/dashboard/api-keys).
2. Install this plugin in Dify.
3. Go to **Settings > Model Provider > EmpirioLabs AI**.
4. Enter your EmpirioLabs AI API key.
5. Select one of the predefined models or add any model from the catalog as a customizable model.

## Models

The plugin includes a small set of predefined chat models:

- `qwen3-7-max`
- `deepseek-v4-pro`
- `kimi-k2-7-code`

For the full current catalog, see [EmpirioLabs AI models](https://empiriolabs.ai/models) or the [models and pricing docs](https://docs.empiriolabs.ai/models-pricing).

## Source and support

- Plugin source: https://github.com/EmpirioLabs-AI/dify-plugin-empiriolabs
- API documentation: https://docs.empiriolabs.ai/
- Product site: https://empiriolabs.ai/
- Support: support@empiriolabs.ai
