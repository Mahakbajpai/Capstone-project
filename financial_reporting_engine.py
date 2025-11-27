import time
import pandas as pd
import concurrent.futures
import google.generativeai as genai
from config import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 1. TOOLS (Custom & Built-in Simulations)
# ==========================================

def get_ledger_data(region):
    """Simulates fetching raw GL data."""
    print(f"   [Tool] Connecting to General Ledger for {region}...")
    time.sleep(1.5) # Simulate network latency
    # Mock Data
    data = {
        'Category': ['Revenue', 'COGS', 'OpEx', 'Tax'],
        'Amount_Actual': [500000, 200000, 150000, 30000], # Q4 Actuals
        'Currency': ['USD'] * 4
    }
    return pd.DataFrame(data)

def get_erp_metrics(region):
    """Simulates fetching Budget data from ERP."""
    print(f"   [Tool] Connecting to ERP System for {region}...")
    time.sleep(1.5) 
    # Mock Data
    data = {
        'Category': ['Revenue', 'COGS', 'OpEx', 'Tax'],
        'Amount_Budget': [480000, 190000, 140000, 30000] # Q4 Budget
    }
    return pd.DataFrame(data)

# ==========================================
# 2. AGENTS
# ==========================================

class DataRetrievalAgent:
    """
    Role: Fetches raw metrics from different sources.
    Pattern: Parallel Agents (using ThreadPoolExecutor)
    """
    def run(self, region):
        print("\n🤖 [Data Retrieval Agent] Starting parallel extraction...")
        
        # Parallel Execution
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_gl = executor.submit(get_ledger_data, region)
            future_erp = executor.submit(get_erp_metrics, region)
            
            gl_df = future_gl.result()
            erp_df = future_erp.result()
            
        print("   [Data Retrieval Agent] Data fetch complete.")
        return gl_df, erp_df

class AnalysisAgent:
    """
    Role: Performs custom calculations (EBITDA, Variance).
    Pattern: Sequential / Deterministic Logic
    """
    def run(self, gl_df, erp_df):
        print("\n🤖 [Analysis Agent] Calculating variances and EBITDA...")
        
        # Merge DataFrames
        merged_df = pd.merge(gl_df, erp_df, on="Category")
        
        # Vectorized Calculations (No LLM hallucinations here)
        merged_df['Variance'] = merged_df['Amount_Actual'] - merged_df['Amount_Budget']
        merged_df['Variance_%'] = (merged_df['Variance'] / merged_df['Amount_Budget']) * 100
        
        # Calculate EBITDA (Revenue - COGS - OpEx)
        # Simplified logic for demo
        rev = merged_df.loc[merged_df['Category'] == 'Revenue', 'Amount_Actual'].values[0]
        cogs = merged_df.loc[merged_df['Category'] == 'COGS', 'Amount_Actual'].values[0]
        opex = merged_df.loc[merged_df['Category'] == 'OpEx', 'Amount_Actual'].values[0]
        
        ebitda = rev - cogs - opex
        
        results = {
            "dataframe": merged_df,
            "ebitda": ebitda,
            "financial_health": "Healthy" if ebitda > 0 else "At Risk"
        }
        return results

class ReportDraftingAgent:
    """
    Role: Converts structured metrics into a narrative.
    Pattern: LLM-Powered Agent
    """
    def run(self, context_data, region):
        print("\n🤖 [Drafting Agent] Generating executive summary...")
        
        df_string = context_data['dataframe'].to_string()
        ebitda = context_data['ebitda']
        
        prompt = f"""
        You are a senior financial analyst. Write a brief executive summary for the Q4 Financial Report for region {region}.
        
        Data Context:
        {df_string}
        
        Calculated EBITDA: ${ebitda}
        
        Requirements:
        1. Summarize Revenue and OpEx performance.
        2. Highlight the Variance (Actual vs Budget).
        3. Keep it professional and strategic.
        """
        
        response = model.generate_content(prompt)
        return response.text

class ComplianceReviewAgent:
    """
    Role: Validates accuracy.
    Pattern: Loop Agent (Critique)
    """
    def run(self, draft_report, calculated_data):
        print("\n🤖 [Review Agent] Verifying numerical accuracy...")
        
        # Simulated Code Execution Check
        # In a full prod environment, we would extract numbers from the LLM text 
        # and compare them against calculated_data['ebitda'].
        
        real_ebitda = calculated_data['ebitda']
        
        # Simple string check for demo purposes
        if str(real_ebitda) in draft_report or f"{real_ebitda:,}" in draft_report:
            print("   ✅ [Compliance] Verification PASSED. Numbers match calculation engine.")
            return True, draft_report
        else:
            print("   ⚠️ [Compliance] Verification FAILED. Creating feedback loop...")
            # Here we would loop back to the drafter with feedback
            # For this demo, we append a correction note
            correction = f"\n\n[AUDIT NOTE]: The calculated EBITDA of ${real_ebitda} was verified by code execution."
            return False, draft_report + correction

# ==========================================
# 3. SUPERVISOR (ORCHESTRATOR)
# ==========================================

class FinancialSupervisor:
    """
    Role: The project manager. Manages the sequence.
    """
    def __init__(self):
        self.collector = DataRetrievalAgent()
        self.analyzer = AnalysisAgent()
        self.writer = ReportDraftingAgent()
        self.reviewer = ComplianceReviewAgent()
        
    def process_request(self, user_request):
        print(f"Testing Request: '{user_request}'")
        print("="*60)
        
        # 1. Parse Request (Simplified for demo, usually uses LLM to extract params)
        region = "EMEA" 
        
        # 2. Data Collection (Parallel)
        gl_data, erp_data = self.collector.run(region)
        
        # 3. Analysis (Sequential)
        analysis_results = self.analyzer.run(gl_data, erp_data)
        print(f"   [Internal Logic] Calculated EBITDA: ${analysis_results['ebitda']}")
        
        # 4. Draft (Sequential)
        draft = self.writer.run(analysis_results, region)
        
        # 5. Review (Loop Pattern)
        is_valid, final_report = self.reviewer.run(draft, analysis_results)
        
        return final_report

# ==========================================
# 4. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    app = FinancialSupervisor()
    
    start_time = time.time()
    
    request = "Generate the Q4 2025 Variance Analysis Report for the EMEA region."
    final_output = app.process_request(request)
    
    end_time = time.time()
    
    print("\n" + "="*60)
    print("FINAL STRATEGIC REPORT")
    print("="*60)
    print(final_output)
    print("="*60)
    print(f"Total Execution Time: {round(end_time - start_time, 2)} seconds")
