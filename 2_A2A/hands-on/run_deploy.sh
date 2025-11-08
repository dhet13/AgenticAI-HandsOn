#!/bin/bash

adk deploy agent_engine shared_news_agent \
  --project="project-test-2-477511" \
  --region="asia-northeast1" \
  --staging_bucket="gs://adk-agent-deploy-bucket-ysh-tokyo" \
  --display_name="google_news_agent_mem"
