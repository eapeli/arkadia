import { useStore } from '@nanostores/react'
import { useMemo } from 'react'

import { Codicon } from '@/components/ui/codicon'
import { useI18n } from '@/i18n'
import { cn } from '@/lib/utils'
import {
  $currentFastMode,
  $currentModel,
  $currentProvider,
  $currentReasoningEffort,
  setModelPickerOpen
} from '@/store/session'

interface ModelCapabilities {
  vision?: boolean
  reasoning?: boolean
  functionCalling?: boolean
  contextLength?: number
  maxOutputTokens?: number
}

interface ModelInfo {
  id: string
  provider: string
  name: string
  capabilities: ModelCapabilities
}

export function ModelSelector({
  model,
  onSelect,
  gateway
}: {
  model: { id: string; provider: string } | null
  onSelect: (model: string, provider: string) => void
  gateway?: any
}) {
  const { t } = useI18n()
  const currentModel = useStore($currentModel)
  const currentProvider = useStore($currentProvider)
  const fastMode = useStore($currentFastMode)
  const reasoningEffort = useStore($currentReasoningEffort)

  // Capabilities database - would come from API in production
  const modelCapabilities = useMemo((): Record<string, ModelCapabilities> => ({
    'gemini-2.5-pro': {
      vision: true,
      reasoning: true,
      functionCalling: true,
      contextLength: 2_000_000,
      maxOutputTokens: 8192
    },
    'gemini-2.5-flash': {
      vision: true,
      reasoning: true,
      functionCalling: true,
      contextLength: 1_000_000,
      maxOutputTokens: 8192
    },
    'gpt-4o': {
      vision: true,
      reasoning: false,
      functionCalling: true,
      contextLength: 128_000,
      maxOutputTokens: 4096
    },
    'gpt-4o-mini': {
      vision: true,
      reasoning: false,
      functionCalling: true,
      contextLength: 128_000,
      maxOutputTokens: 16384
    },
    'claude-3-5-sonnet': {
      vision: true,
      reasoning: false,
      functionCalling: true,
      contextLength: 200_000,
      maxOutputTokens: 8192
    },
    'claude-3-5-haiku': {
      vision: true,
      reasoning: false,
      functionCalling: true,
      contextLength: 200_000,
      maxOutputTokens: 8192
    },
    'deepseek-chat': {
      vision: false,
      reasoning: true,
      functionCalling: true,
      contextLength: 64_000,
      maxOutputTokens: 8192
    },
    'deepseek-reasoner': {
      vision: false,
      reasoning: true,
      functionCalling: true,
      contextLength: 64_000,
      maxOutputTokens: 8192
    },
    'nemotron-3-ultra': {
      vision: false,
      reasoning: true,
      functionCalling: true,
      contextLength: 128_000,
      maxOutputTokens: 4096
    }
  }), [])

  const capabilities = model ? modelCapabilities[model.id] : null

  const formatCapabilities = (caps: ModelCapabilities) => {
    const items: string[] = []
    if (caps.vision) items.push('🖼️ Vision')
    if (caps.reasoning) items.push('🧠 Reasoning')
    if (caps.functionCalling) items.push('🔧 Tools')
    if (caps.contextLength) items.push(`${Math.round(caps.contextLength / 1000)}k ctx`)
    return items.join(' · ')
  }

  if (!model) {
    return (
      <button
        className={cn(
          'flex h-(--composer-control-size) max-w-40 shrink-0 items-center gap-1 rounded-md px-2 text-xs font-normal',
          'text-(--ui-text-tertiary) hover:bg-(--chrome-action-hover) hover:text-foreground'
        )}
        onClick={() => setModelPickerOpen(true)}
        title={t.shell.statusbar.openModelPicker}
      >
        <span className="truncate">{t.shell.statusbar.selectModel}</span>
        <Codicon name="chevron-down" size="2.5" className="shrink-0 opacity-50" />
      </button>
    )
  }

  return (
    <div className="relative">
      <button
        className={cn(
          'flex h-(--composer-control-size) max-w-48 shrink-0 items-center gap-1.5 rounded-md px-2 text-xs font-normal',
          'text-(--ui-text-secondary) hover:bg-(--chrome-action-hover) hover:text-foreground'
        )}
        onClick={() => setModelPickerOpen(true)}
        title={`${model.provider} · ${model.id}`}
      >
        <span className="truncate">{model.id}</span>
        <Codicon name="chevron-down" size="2.5" className="shrink-0 opacity-50" />
      </button>

      {/* Capabilities tooltip */}
      {capabilities && (
        <div className="absolute bottom-full left-0 mb-1 hidden group-hover:block">
          <div className="rounded-md bg-(--ui-popover-background) px-3 py-2 text-xs text-(--ui-text-secondary) shadow-lg border border-(--ui-stroke-tertiary) whitespace-nowrap">
            {formatCapabilities(capabilities)}
          </div>
        </div>
      )}
    </div>
  )
}

export function ModelPickerPanel({
  onSelect,
  gateway
}: {
  onSelect: (model: string, provider: string) => void
  gateway?: any
}) {
  const { t } = useI18n()

  // Mock model data - would come from API
  const models = useMemo(() => [
    { provider: 'google', name: 'Google', models: [
      { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', capabilities: { vision: true, reasoning: true, tools: true, context: '2M' }},
      { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', capabilities: { vision: true, reasoning: true, tools: true, context: '1M' }},
      { id: 'gemini-1.5-pro', name: 'Gemini 1.5 Pro', capabilities: { vision: true, reasoning: false, tools: true, context: '2M' }},
      { id: 'gemini-1.5-flash', name: 'Gemini 1.5 Flash', capabilities: { vision: true, reasoning: false, tools: true, context: '1M' }},
    ]},
    { provider: 'openai', name: 'OpenAI', models: [
      { id: 'gpt-4o', name: 'GPT-4o', capabilities: { vision: true, reasoning: false, tools: true, context: '128k' }},
      { id: 'gpt-4o-mini', name: 'GPT-4o Mini', capabilities: { vision: true, reasoning: false, tools: true, context: '128k' }},
      { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', capabilities: { vision: true, reasoning: false, tools: true, context: '128k' }},
    ]},
    { provider: 'anthropic', name: 'Anthropic', models: [
      { id: 'claude-3-5-sonnet', name: 'Claude 3.5 Sonnet', capabilities: { vision: true, reasoning: false, tools: true, context: '200k' }},
      { id: 'claude-3-5-haiku', name: 'Claude 3.5 Haiku', capabilities: { vision: true, reasoning: false, tools: true, context: '200k' }},
    ]},
    { provider: 'deepseek', name: 'DeepSeek', models: [
      { id: 'deepseek-chat', name: 'DeepSeek V3', capabilities: { vision: false, reasoning: true, tools: true, context: '64k' }},
      { id: 'deepseek-reasoner', name: 'DeepSeek R1', capabilities: { vision: false, reasoning: true, tools: true, context: '64k' }},
    ]},
    { provider: 'nvidia', name: 'NVIDIA', models: [
      { id: 'nemotron-3-ultra', name: 'Nemotron 3 Ultra', capabilities: { vision: false, reasoning: true, tools: true, context: '128k' }},
    ]},
  ], [])

  return (
    <div className="w-72">
      <div className="p-2 border-b border-(--ui-stroke-tertiary)">
        <input
          type="search"
          placeholder={t.shell.modelMenu.search}
          className="w-full rounded-md border border-(--ui-stroke-tertiary) bg-(--ui-popover-background) px-3 py-1.5 text-xs text-(--ui-text-primary) placeholder:text-(--ui-text-tertiary) focus:border-(--ui-accent) focus:outline-none focus:ring-1 focus:ring-(--ui-accent)"
        />
      </div>
      <div className="max-h-80 overflow-y-auto">
        {models.map((providerGroup) => (
          <div key={providerGroup.provider} className="py-1">
            <div className="px-2 py-1 text-[2 py-1.5 text-xs font-medium text-(--ui-text-tertiary) uppercase tracking-wider">
              {providerGroup.name}
            </div>
            {providerGroup.models.map((m) => (
              <button
                key={m.id}
                className={cn(
                  'w-full flex items-center gap-2 px-2 py-1.5 text-left text-sm rounded-md hover:bg-(--ui-control-hover-background) transition-colors',
                  currentModel === m.id && currentProvider === providerGroup.provider
                    ? 'bg-(--ui-control-active-background) text-foreground'
                    : 'text-(--ui-text-secondary)'
                )}
                onClick={() => onSelect(m.id, providerGroup.provider)}
              >
                <span className="flex-1 truncate font-medium">{m.name}</span>
                <span className="flex items-center gap-1 text-[0.625rem] text-(--ui-text-tertiary)">
                  {m.capabilities.vision && <Codicon name="eye" size="10" title="Vision" />}
                  {m.capabilities.reasoning && <Codicon name="lightbulb" size="10" title="Reasoning" />}
                  {m.capabilities.tools && <Codicon name="tools" size="10" title="Tools" />}
                  <span className="text-(--ui-text-quaternary)">{m.capabilities.context}</span>
                </span>
              </button>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}