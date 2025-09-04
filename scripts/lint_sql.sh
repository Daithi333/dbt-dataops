#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Linting all dbt projects..."
for project in dbt_projects/*; do
  echo "📂 $project"
  sqlfluff lint "$project" --dialect postgres --templater dbt
done


echo "✅ SQL linting & fixing complete"
