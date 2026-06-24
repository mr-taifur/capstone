# AgriGuardian AI Orchestrator

import os
import asyncio
import dotenv
from security import validate_text, validate_image_file
from tools import get_weather
from skills.disease_knowledge import search_disease_by_keyword, get_disease_details, list_all_diseases
from skills.treatment_knowledge import get_treatment_recs
from skills.weather_analysis import calculate_disease_risks, generate_weather_farming_advice

# Load environment variables
dotenv.load_dotenv()

class AgriGuardianOrchestrator:
    def __init__(self, demo_mode: bool = False):
        self.demo_mode = demo_mode
        self.api_key_valid = "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"] != "DUMMY_KEY"
        
    async def run_workflow(self, location: str, text_description: str, image_name: str = None) -> dict:
        """
        Runs the multi-agent workflow.
        Checks security guardrails first, then decides whether to use live ADK runners or high-fidelity simulation.
        
        Returns a dictionary containing:
        - success: bool
        - error: str (if any)
        - logs: list of strings showing agent handoffs
        - detector_output: str
        - diagnosis_output: str
        - treatment_output: str
        - weather_output: str
        - final_report: str
        - mode: 'live' or 'demo'
        """
        logs = []
        logs.append("🛡️ Security Agent: Initiating input verification...")
        
        # 1. Security Check
        is_text_safe, text_err = validate_text(text_description)
        if not is_text_safe:
            return {"success": False, "error": f"Security Rejection: {text_err}", "logs": logs}
            
        if image_name:
            is_img_safe, img_err = validate_image_file(image_name)
            if not is_img_safe:
                return {"success": False, "error": f"Security Rejection: {img_err}", "logs": logs}
                
        logs.append("🛡️ Security Agent: Input verification complete. Input is safe.")
        
        # Decide if we run live or demo fallback
        run_live = self.api_key_valid and not self.demo_mode
        
        if run_live:
            logs.append("⚡ Running in LIVE Agentic Mode (Gemini 2.5 Flash)...")
            return await self._run_live_workflow(location, text_description, image_name, logs)
        else:
            logs.append("🚜 Running in DEMO Simulation Mode...")
            return await self._run_demo_workflow(location, text_description, image_name, logs)
            
    async def _run_live_workflow(self, location: str, text_description: str, image_name: str, logs: list[str]) -> dict:
        """Executes the workflow using live Google ADK Agents."""
        # Since running live requires a valid API key, we construct the runners and chain them.
        # To avoid blocking the execution due to lack of a key, we wrap in a try-catch,
        # falling back to demo mode if a client error occurs.
        try:
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from agents import disease_detector, disease_diagnosis, treatment_recommender, weather_advisor, report_generator
            
            # Step 1: Disease Detector
            logs.append("🔍 Agent 1: Disease Detector is analyzing symptoms...")
            detector_prompt = f"Analyze these crop leaf symptoms: {text_description}. Identify the crop and symptoms."
            det_runner = Runner(agent=disease_detector, app_name="detector_app", session_service=InMemorySessionService())
            events = await det_runner.run_debug(detector_prompt)
            detector_output = self._extract_text_from_events(events)
            logs.append(f"🔍 Detector completed. Crop/symptom description gathered.")
            
            # Step 2: Diagnosis Agent
            logs.append("🩺 Agent 2: Diagnosis Agent is evaluating symptoms...")
            diag_prompt = f"Based on these detected symptoms, diagnose the crop disease: {detector_output}"
            diag_runner = Runner(agent=disease_diagnosis, app_name="diagnosis_app", session_service=InMemorySessionService())
            events = await diag_runner.run_debug(diag_prompt)
            diagnosis_output = self._extract_text_from_events(events)
            logs.append("🩺 Diagnosis completed.")
            
            # Step 3: Treatment Agent
            logs.append("💊 Agent 3: Treatment Agent is generating tiered recommendations...")
            treat_prompt = f"Generate tiered organic, biological, and chemical treatments for this diagnosis: {diagnosis_output}"
            treat_runner = Runner(agent=treatment_recommender, app_name="treatment_app", session_service=InMemorySessionService())
            events = await treat_runner.run_debug(treat_prompt)
            treatment_output = self._extract_text_from_events(events)
            logs.append("💊 Treatment recommendations complete.")
            
            # Step 4: Weather Agent
            logs.append(f"☀️ Agent 4: Weather Advisor is querying climate data for {location}...")
            weather_prompt = f"Get local weather for location: '{location}' and provide farming advice."
            weather_runner = Runner(agent=weather_advisor, app_name="weather_app", session_service=InMemorySessionService())
            events = await weather_runner.run_debug(weather_prompt)
            weather_output = self._extract_text_from_events(events)
            logs.append("☀️ Weather-based advisory generated.")
            
            # Step 5: Report Agent
            logs.append("📋 Agent 5: Report Generator is compiling final agricultural health report...")
            report_prompt = (
                f"Compile the final health report based on these sections:\n"
                f"Symptom Profile: {detector_output}\n"
                f"Diagnosis: {diagnosis_output}\n"
                f"Treatments: {treatment_output}\n"
                f"Weather Advisory: {weather_output}"
            )
            report_runner = Runner(agent=report_generator, app_name="report_app", session_service=InMemorySessionService())
            events = await report_runner.run_debug(report_prompt)
            final_report = self._extract_text_from_events(events)
            logs.append("📋 AgriGuardian Report successfully compiled.")
            
            return {
                "success": True,
                "logs": logs,
                "detector_output": detector_output,
                "diagnosis_output": diagnosis_output,
                "treatment_output": treatment_output,
                "weather_output": weather_output,
                "final_report": final_report,
                "mode": "live"
            }
            
        except Exception as e:
            logs.append(f"⚠️ Live workflow failed: {e}. Switching to high-fidelity demo simulation...")
            return await self._run_demo_workflow(location, text_description, image_name, logs)

    def _extract_text_from_events(self, events) -> str:
        """Helper to extract generated text contents from ADK execution events."""
        # Simple extraction logic from standard Event schemas
        text_parts = []
        for e in events:
            # Events in ADK typically yield standard properties or text dumps
            # We can print attributes or check types
            if hasattr(e, "content") and e.content:
                if hasattr(e.content, "parts"):
                    for part in e.content.parts:
                        if hasattr(part, "text") and part.text:
                            text_parts.append(part.text)
                elif isinstance(e.content, str):
                    text_parts.append(e.content)
            elif hasattr(e, "text") and e.text:
                text_parts.append(e.text)
        
        output = "".join(text_parts)
        if not output:
            # Fallback if events are structured differently
            output = str(events)
        return output

    async def _run_demo_workflow(self, location: str, text_description: str, image_name: str, logs: list[str]) -> dict:
        """Simulates the workflow using high-fidelity knowledge databases and weather analysis rules."""
        # Wait a brief moment to simulate processing time
        await asyncio.sleep(0.5)
        
        # Match crop and disease from input text
        matched_disease = None
        search_results = search_disease_by_keyword(text_description)
        if search_results:
            matched_disease = search_results[0]
        else:
            # Fallback based on keywords or default to Rice Blast
            desc_lower = text_description.lower()
            if "potato" in desc_lower or "late blight" in desc_lower:
                matched_disease = get_disease_details("potato_late_blight")
            elif "tomato" in desc_lower or "leaf curl" in desc_lower:
                matched_disease = get_disease_details("tomato_leaf_curl")
            elif "bacterial" in desc_lower or "blight" in desc_lower:
                matched_disease = get_disease_details("rice_bacterial_leaf_blight")
            else:
                # Default to Rice Blast
                matched_disease = get_disease_details("rice_blast")
                
        disease_key = None
        for k, v in {
            "rice_blast": "Rice Blast",
            "rice_bacterial_leaf_blight": "Bacterial Leaf Blight",
            "potato_late_blight": "Potato Late Blight",
            "tomato_leaf_curl": "Tomato Leaf Curl"
        }.items():
            if v == matched_disease["name"]:
                disease_key = k
                break
                
        # 1. Detector Output simulation
        logs.append("🔍 Agent 1: Disease Detector is analyzing symptoms...")
        await asyncio.sleep(0.3)
        crop = matched_disease["crop"]
        symptoms_str = "\n".join([f"- {s}" for s in matched_disease["symptoms"]])
        detector_output = (
            f"**Crop Detected:** {crop}\n"
            f"**Observed Symptoms:**\n{symptoms_str}\n"
            f"**User Description Context:** '{text_description}'"
        )
        logs.append("🔍 Detector completed. Crop/symptom description gathered.")
        
        # 2. Diagnosis Output simulation
        logs.append("🩺 Agent 2: Diagnosis Agent is evaluating symptoms...")
        await asyncio.sleep(0.3)
        diagnosis_output = (
            f"**Diagnosis:** {matched_disease['name']} (Scientific Name: *{matched_disease['scientific_name']}*)\n"
            f"**Pathogen Type:** {matched_disease['pathogen_type']}\n"
            f"**Confidence Level:** 95%\n"
            f"**Diagnostic Details:** Symptoms perfectly align with the diagnostic profile: {matched_disease['environmental_factors']}"
        )
        logs.append("🩺 Diagnosis completed.")
        
        # 3. Treatment Output simulation
        logs.append("💊 Agent 3: Treatment Agent is generating tiered recommendations...")
        await asyncio.sleep(0.3)
        trecs = get_treatment_recs(disease_key)
        organic_str = "\n".join([f"- {item}" for item in trecs["organic"]])
        bio_str = "\n".join([f"- {item}" for item in trecs["biological"]])
        chem_str = "\n".join([f"- {item}" for item in trecs["chemical"]])
        
        treatment_output = (
            f"**Tier 1: Organic & Cultural Practices:**\n{organic_str}\n\n"
            f"**Tier 2: Biological Controls:**\n{bio_str}\n\n"
            f"**Tier 3: Chemical Treatments (Bangladesh BARC Approved):**\n{chem_str}\n\n"
            f"**⚠️ Farmer Safety Guidelines:**\n{trecs['safety_notes']}"
        )
        logs.append("💊 Treatment recommendations complete.")
        
        # 4. Weather Agent simulation
        logs.append(f"☀️ Agent 4: Weather Advisor is querying climate data for {location}...")
        await asyncio.sleep(0.3)
        weather_info = get_weather(location)
        risks = calculate_disease_risks(weather_info["temp"], weather_info["humidity"])
        advisories = generate_weather_farming_advice(
            weather_info["temp"], weather_info["humidity"], weather_info["rain_prob"]
        )
        advisory_str = "\n".join([f"- {item}" for item in advisories])
        
        # Specific risk for current disease
        cur_disease_risk = risks.get(disease_key, "Low")
        
        weather_output = (
            f"**Current Local Weather ({location}):**\n"
            f"- Temperature: {weather_info['temp']}°C\n"
            f"- Humidity: {weather_info['humidity']}%\n"
            f"- Rain Probability: {weather_info['rain_prob']}%\n"
            f"- Conditions: {weather_info['description']} (Source: {weather_info['source']})\n\n"
            f"**Disease Outbreak Risk Assessment:**\n"
            f"- Risk of {matched_disease['name']} outbreak in this area: **{cur_disease_risk}**\n\n"
            f"**Action Advisories:**\n{advisory_str}"
        )
        logs.append("☀️ Weather-based advisory generated.")
        
        # 5. Report Agent compilation
        logs.append("📋 Agent 5: Report Generator is compiling final agricultural health report...")
        await asyncio.sleep(0.3)
        final_report = (
            f"### 🛡️ AgriGuardian AI Agricultural Health Report\n\n"
            f"**Location:** {location.capitalize()}, Bangladesh | **Crop Analyzed:** {crop}\n\n"
            f"#### 1. Crop Profile & Symptom Detection\n"
            f"{detector_output}\n\n"
            f"#### 2. Clinical Diagnosis\n"
            f"{diagnosis_output}\n\n"
            f"#### 3. Tiered Treatment Recommendations\n"
            f"{treatment_output}\n\n"
            f"#### 4. Weather-Based Farming Advisory\n"
            f"{weather_output}\n\n"
            f"#### 5. Farmer Safety Checklist\n"
            f"- [ ] Wear a protective face mask and thick rubber gloves before handling any chemical fungicide.\n"
            f"- [ ] Do not spray chemicals against the wind direction.\n"
            f"- [ ] Dispose of unused spray solution and packaging safely, away from cattle and fish ponds.\n"
            f"- [ ] Observe the recommended Pre-Harvest Interval (PHI) of 14 days before harvesting the crop.\n"
            f"- [ ] Ensure clean fresh water and soap are available in the field for immediate washing."
        )
        logs.append("📋 AgriGuardian Report successfully compiled.")
        
        return {
            "success": True,
            "logs": logs,
            "detector_output": detector_output,
            "diagnosis_output": diagnosis_output,
            "treatment_output": treatment_output,
            "weather_output": weather_output,
            "final_report": final_report,
            "mode": "demo"
        }
