#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'yaml'
require 'time'
require 'optparse'
require 'fileutils'

def squeeze_text(text)
  text.to_s.gsub(/\s+/, ' ').strip
end

def fit(text, max_len)
  normalized = squeeze_text(text)
  return normalized if normalized.length <= max_len

  normalized[0...max_len]
end

def first_present(*values)
  values.find { |value| !squeeze_text(value).empty? }.to_s
end

def short_phrase(text, max_len = 10)
  fit(text, max_len)
end

def uniq_fill(items, target_size, fallback_pool)
  output = []
  (items + fallback_pool).each do |item|
    next if item.nil?

    text = squeeze_text(item)
    next if text.empty?
    next if output.include?(text)

    output << text
    break if output.length >= target_size
  end
  output
end

def brief_context(brief)
  primary_keywords = Array(brief.dig('keyword_cluster', 'primary_keywords')).map { |value| squeeze_text(value) }
  secondary_keywords = Array(brief.dig('keyword_cluster', 'secondary_keywords')).map { |value| squeeze_text(value) }
  supporting_points = Array(brief.dig('landing_page_summary', 'supporting_points')).map { |value| squeeze_text(value) }
  usps = Array(brief['usp']).map { |value| squeeze_text(value) }
  pain_points = Array(brief.dig('target_audience', 'pain_points')).map { |value| squeeze_text(value) }
  outcomes = Array(brief.dig('target_audience', 'desired_outcomes')).map { |value| squeeze_text(value) }

  {
    brand_name: squeeze_text(brief['brand_name']),
    product_name: squeeze_text(brief['product_name']),
    campaign_type: squeeze_text(brief['campaign_type']),
    brief_id: squeeze_text(brief['brief_id']),
    primary_keyword: first_present(primary_keywords[0], brief['product_name']),
    secondary_keyword: first_present(primary_keywords[1], secondary_keywords[0], brief['product_name']),
    tertiary_keyword: first_present(primary_keywords[2], secondary_keywords[1], brief['product_name']),
    cta: first_present(brief.dig('landing_page_summary', 'primary_cta'), '立即了解'),
    support_a: first_present(supporting_points[0], usps[0], brief.dig('landing_page_summary', 'primary_cta')),
    support_b: first_present(supporting_points[1], usps[1], outcomes[0]),
    support_c: first_present(supporting_points[2], usps[2], outcomes[1]),
    usp_a: first_present(usps[0], supporting_points[0], brief['product_name']),
    usp_b: first_present(usps[1], supporting_points[1], brief['product_name']),
    pain_a: first_present(pain_points[0], brief.dig('landing_page_summary', 'hero_message')),
    pain_b: first_present(pain_points[1], outcomes[0]),
    outcome_a: first_present(outcomes[0], supporting_points[0], brief['product_name']),
    outcome_b: first_present(outcomes[1], supporting_points[1], brief['product_name'])
  }
end

def search_angles(ctx)
  [
    {
      'key' => 'product_truth',
      'label' => '產品事實',
      'rationale' => "#{ctx[:primary_keyword]}、#{short_phrase(ctx[:usp_a], 16)} 與產品核心特性。"
    },
    {
      'key' => 'pain_to_relief',
      'label' => '痛點放鬆',
      'rationale' => "#{short_phrase(ctx[:pain_a], 14)} 與 #{short_phrase(ctx[:outcome_a], 14)} 的對應。"
    },
    {
      'key' => 'trust_cta',
      'label' => '信任行動',
      'rationale' => "#{short_phrase(ctx[:support_a], 14)} 搭配 #{short_phrase(ctx[:cta], 10)}。"
    }
  ]
end

def pmax_angles(ctx)
  [
    {
      'key' => 'product_truth',
      'label' => '產品事實',
      'rationale' => "#{ctx[:primary_keyword]} 與 #{short_phrase(ctx[:usp_a], 16)} 可作為 PMax 重組基底。"
    },
    {
      'key' => 'pain_to_relief',
      'label' => '痛點放鬆',
      'rationale' => "#{short_phrase(ctx[:pain_a], 14)} 到 #{short_phrase(ctx[:outcome_a], 14)} 的情境推進。"
    },
    {
      'key' => 'trust_cta',
      'label' => '信任行動',
      'rationale' => "#{short_phrase(ctx[:support_a], 14)}、#{short_phrase(ctx[:support_b], 14)} 與 #{short_phrase(ctx[:cta], 10)}。"
    }
  ]
end

def search_headlines(ctx)
  candidates = [
    fit("#{ctx[:brand_name]} #{ctx[:primary_keyword]}", 30),
    fit("#{ctx[:secondary_keyword]} 先試再選", 30),
    fit("#{ctx[:primary_keyword]} 看#{short_phrase(ctx[:usp_a], 8)}", 30),
    fit("#{ctx[:tertiary_keyword]} 更貼近需求", 30),
    fit(ctx[:support_a], 30),
    fit("#{short_phrase(ctx[:pain_a], 10)} 找對支撐", 30),
    fit("#{short_phrase(ctx[:pain_b], 10)} 先別急著買", 30),
    fit('讓身體先被接住', 30),
    fit(short_phrase(ctx[:outcome_a], 14), 30),
    fit('晚安歡迎回家 好好睡', 30),
    fit("#{short_phrase(ctx[:cta], 12)} 找到合適選擇", 30),
    fit("#{ctx[:brand_name]} #{short_phrase(ctx[:cta], 12)}", 30),
    fit(short_phrase(ctx[:support_b], 14), 30),
    fit(short_phrase(ctx[:support_c], 14), 30),
    fit('用體驗做選擇 更放心', 30)
  ]
  uniq_fill(candidates, 15, ['找到更適合的睡感', '先感受再決定'])
end

def search_descriptions(ctx)
  uniq_fill([
    fit("#{ctx[:brand_name]}用#{short_phrase(ctx[:support_a], 16)}陪你比較差異，先感受再決定。", 90),
    fit("從#{short_phrase(ctx[:primary_keyword], 14)}到#{short_phrase(ctx[:usp_b], 16)}，慢慢找到更適合自己的選擇。", 90),
    fit("如果你常常#{short_phrase(ctx[:pain_a], 16)}，歡迎先用體驗感受更安心的支撐與放鬆。", 90),
    fit("#{short_phrase(ctx[:cta], 14)}後，再用自己的身體感受#{short_phrase(ctx[:outcome_a], 16)}。", 90)
  ], 4, ['先體驗再決定，讓選擇更安心。'])
end

def pmax_short_headlines(ctx)
  uniq_fill([
    fit("#{ctx[:brand_name]} #{ctx[:primary_keyword]}", 30),
    fit("#{ctx[:secondary_keyword]} 先試再選", 30),
    fit("#{ctx[:primary_keyword]} 更貼近需求", 30),
    fit(ctx[:support_a], 30),
    fit(ctx[:support_b], 30),
    fit("#{short_phrase(ctx[:pain_a], 10)} 找對支撐", 30),
    fit("#{short_phrase(ctx[:pain_b], 10)} 先感受差異", 30),
    fit('讓身體先被接住', 30),
    fit(short_phrase(ctx[:outcome_a], 14), 30),
    fit(short_phrase(ctx[:outcome_b], 14), 30),
    fit("#{short_phrase(ctx[:cta], 12)} 更安心", 30),
    fit("#{ctx[:brand_name]} #{short_phrase(ctx[:cta], 12)}", 30),
    fit('用體驗做選擇 更放心', 30),
    fit('先來感受差異', 30),
    fit('找到適合自己的睡感', 30)
  ], 15, ['慢慢找到適合自己的選擇'])
end

def pmax_long_headlines(ctx)
  uniq_fill([
    fit("從#{short_phrase(ctx[:primary_keyword], 14)}到#{short_phrase(ctx[:usp_a], 18)}，先感受再決定。", 90),
    fit("如果你常常#{short_phrase(ctx[:pain_a], 16)}，歡迎先用體驗慢慢找到更適合的放鬆節奏。", 90),
    fit("#{ctx[:brand_name]}把#{short_phrase(ctx[:support_a], 16)}與#{short_phrase(ctx[:support_b], 16)}放進同一段選購流程。", 90),
    fit("#{short_phrase(ctx[:cta], 14)}後，再用自己的身體感受#{short_phrase(ctx[:outcome_a], 18)}。", 90),
    fit('這不是只看價格的快選流程，而是讓你先體驗，再決定什麼更適合自己。', 90)
  ], 5, ['先體驗，再找到更適合自己的選擇。'])
end

def pmax_descriptions(ctx)
  uniq_fill([
    fit(short_phrase(ctx[:cta], 12), 60),
    fit("#{ctx[:brand_name]}用#{short_phrase(ctx[:support_a], 16)}陪你比較差異，先感受再決定。", 90),
    fit("從#{short_phrase(ctx[:primary_keyword], 14)}到#{short_phrase(ctx[:usp_b], 16)}，讓身體先被接住。", 90),
    fit("如果你常常#{short_phrase(ctx[:pain_a], 16)}，歡迎先感受更穩定的支撐與放鬆節奏。", 90),
    fit("先用體驗感受#{short_phrase(ctx[:outcome_a], 16)}，再決定下一步是否把它帶回家。", 90)
  ], 5, ['先來感受差異。'])
end

def search_output(brief, ctx)
  angles = search_angles(ctx)
  headlines = search_headlines(ctx)
  descriptions = search_descriptions(ctx)

  {
    'task_id' => 'gads-copy-003',
    'brief_id' => brief['brief_id'],
    'campaign_type' => 'search_rsa',
    'brand_name' => brief['brand_name'],
    'product_name' => brief['product_name'],
    'generated_by' => 'codex',
    'generated_at' => Time.now.iso8601,
    'angles' => angles,
    'headlines' => headlines.each_with_index.map do |text, index|
      {
        'text' => text,
        'angle_key' => angles[index / 5]['key'],
        'keyword_used' => index < 4
      }
    end,
    'descriptions' => descriptions.each_with_index.map do |text, index|
      {
        'text' => text,
        'angle_key' => angles[[index, 2].min]['key']
      }
    end,
    'compliance_notes' => {
      'manual_review_required' => true,
      'checks_passed' => ['draft_generated_from_brief', 'counts_targeted', 'brand_rules_loaded'],
      'policy_risks' => ['自動草稿仍需人工確認是否有接近醫療或誇大語意'],
      'brand_risks' => ['自動草稿可能較模板化，仍需人工調整語氣與落地頁承接']
    }
  }
end

def pmax_output(brief, ctx)
  angles = pmax_angles(ctx)
  short_headlines = pmax_short_headlines(ctx)
  long_headlines = pmax_long_headlines(ctx)
  descriptions = pmax_descriptions(ctx)

  {
    'task_id' => 'gads-copy-003',
    'brief_id' => brief['brief_id'],
    'campaign_type' => 'pmax',
    'brand_name' => brief['brand_name'],
    'product_name' => brief['product_name'],
    'generated_by' => 'codex',
    'generated_at' => Time.now.iso8601,
    'angles' => angles,
    'short_headlines' => short_headlines.each_with_index.map do |text, index|
      {
        'text' => text,
        'angle_key' => angles[index / 5]['key'],
        'keyword_used' => index < 4
      }
    end,
    'long_headlines' => long_headlines.each_with_index.map do |text, index|
      {
        'text' => text,
        'angle_key' => angles[[index, 2].min]['key']
      }
    end,
    'descriptions' => descriptions.each_with_index.map do |text, index|
      {
        'text' => text,
        'angle_key' => angles[[index, 2].min]['key']
      }
    end,
    'compliance_notes' => {
      'manual_review_required' => true,
      'checks_passed' => ['draft_generated_from_brief', 'counts_targeted', 'brand_rules_loaded'],
      'policy_risks' => ['自動草稿仍需人工確認是否有接近醫療或誇大語意'],
      'brand_risks' => ['PMax 資產重組情境仍需人工檢查是否過度模板化']
    }
  }
end

def render_search_markdown(output)
  lines = []
  lines << '# Search RSA Copy Pack'
  lines << ''
  lines << "**Task ID**: #{output['task_id']}  "
  lines << "**Brief ID**: #{output['brief_id']}  "
  lines << "**Brand**: #{output['brand_name']}  "
  lines << "**Product**: #{output['product_name']}  "
  lines << "**Campaign Type**: #{output['campaign_type']}  "
  lines << "**Generated By**: #{output['generated_by']}  "
  lines << "**Generated At**: #{output['generated_at']}"
  lines << ''
  lines << '## Angles'
  lines << ''
  lines << '| Key | Label | Rationale |'
  lines << '|-----|-------|-----------|'
  output['angles'].each do |angle|
    lines << "| #{angle['key']} | #{angle['label']} | #{angle['rationale']} |"
  end
  lines << ''
  lines << '## Headlines'
  lines << ''
  output['headlines'].each_with_index do |item, index|
    lines << "#{index + 1}. #{item['text']} [#{item['angle_key']}]"
  end
  lines << ''
  lines << '## Descriptions'
  lines << ''
  output['descriptions'].each_with_index do |item, index|
    lines << "#{index + 1}. #{item['text']} [#{item['angle_key']}]"
  end
  lines << ''
  lines << '## Compliance Notes'
  lines << ''
  lines << "- Checks passed: #{output.dig('compliance_notes', 'checks_passed').join(', ')}"
  lines << "- Policy risks: #{output.dig('compliance_notes', 'policy_risks').join(' / ')}"
  lines << "- Brand risks: #{output.dig('compliance_notes', 'brand_risks').join(' / ')}"
  lines << "- Manual review required: #{output.dig('compliance_notes', 'manual_review_required')}"
  lines.join("\n")
end

def render_pmax_markdown(output)
  lines = []
  lines << '# PMax Copy Pack'
  lines << ''
  lines << "**Task ID**: #{output['task_id']}  "
  lines << "**Brief ID**: #{output['brief_id']}  "
  lines << "**Brand**: #{output['brand_name']}  "
  lines << "**Product**: #{output['product_name']}  "
  lines << "**Campaign Type**: #{output['campaign_type']}  "
  lines << "**Generated By**: #{output['generated_by']}  "
  lines << "**Generated At**: #{output['generated_at']}"
  lines << ''
  lines << '## Angles'
  lines << ''
  lines << '| Key | Label | Rationale |'
  lines << '|-----|-------|-----------|'
  output['angles'].each do |angle|
    lines << "| #{angle['key']} | #{angle['label']} | #{angle['rationale']} |"
  end
  lines << ''
  lines << '## Short Headlines'
  lines << ''
  output['short_headlines'].each_with_index do |item, index|
    lines << "#{index + 1}. #{item['text']} [#{item['angle_key']}]"
  end
  lines << ''
  lines << '## Long Headlines'
  lines << ''
  output['long_headlines'].each_with_index do |item, index|
    lines << "#{index + 1}. #{item['text']} [#{item['angle_key']}]"
  end
  lines << ''
  lines << '## Descriptions'
  lines << ''
  output['descriptions'].each_with_index do |item, index|
    lines << "#{index + 1}. #{item['text']} [#{item['angle_key']}]"
  end
  lines << ''
  lines << '## Compliance Notes'
  lines << ''
  lines << "- Checks passed: #{output.dig('compliance_notes', 'checks_passed').join(', ')}"
  lines << "- Policy risks: #{output.dig('compliance_notes', 'policy_risks').join(' / ')}"
  lines << "- Brand risks: #{output.dig('compliance_notes', 'brand_risks').join(' / ')}"
  lines << "- Manual review required: #{output.dig('compliance_notes', 'manual_review_required')}"
  lines.join("\n")
end

def load_brief(path)
  ext = File.extname(path)
  content = File.read(path)
  ext == '.json' ? JSON.parse(content) : YAML.safe_load(content)
end

options = { output_dir: nil }

OptionParser.new do |opts|
  opts.banner = 'Usage: batch_generate_ads_copy.rb [options] brief1.yaml brief2.yaml ...'
  opts.on('--output-dir DIR', 'Where to write generated JSON and Markdown files') do |value|
    options[:output_dir] = value
  end
end.parse!

brief_paths = ARGV
if brief_paths.empty?
  brief_paths = Dir['ai/testcases/google-ads/*search.yaml'] + Dir['ai/testcases/google-ads/*pmax.yaml']
end

abort('No brief files found.') if brief_paths.empty?
abort('Please provide --output-dir DIR') if options[:output_dir].to_s.empty?

FileUtils.mkdir_p(options[:output_dir])

brief_paths.sort.each do |path|
  brief = load_brief(path)
  ctx = brief_context(brief)
  output =
    case brief['campaign_type']
    when 'search_rsa' then search_output(brief, ctx)
    when 'pmax' then pmax_output(brief, ctx)
    else
      warn("Skip unsupported campaign_type in #{path}")
      next
    end

  basename = File.basename(path, File.extname(path))
  json_path = File.join(options[:output_dir], "#{basename}.output.json")
  md_path = File.join(options[:output_dir], "#{basename}.output.md")

  File.write(json_path, JSON.pretty_generate(output))
  markdown = output['campaign_type'] == 'search_rsa' ? render_search_markdown(output) : render_pmax_markdown(output)
  File.write(md_path, markdown)

  puts "Generated #{json_path}"
  puts "Generated #{md_path}"
end
