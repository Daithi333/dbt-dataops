#!/usr/bin/env bash
set -euo pipefail

echo "🛠 Attempting to fix all dbt projects..."
for project in dbt_projects/*; do
  echo "📂 $project"
  sqlfluff fix "$project" --dialect postgres --templater dbt --force
done

echo "✅ Done. Run scripts/lint.sh to check remaining issues."
