SCENARIOS = [
    {
        "id": 1,
        "intent": "Request a meeting with a new client",
        "facts": ["First interaction after LinkedIn connection", "Want to discuss digital transformation", "Available Mon-Wed next week", "Meeting duration: 30 minutes"],
        "tone": "Professional and confident",
        "human_reference": "Subject: Introduction - Discussing your Digital Transformation Goals\n\nHi [Name],\n\nIt was great connecting with you on LinkedIn recently. I'm reaching out because I'd love to learn more about your current initiatives and discuss how we might support your digital transformation goals.\n\nCould we schedule a brief 30-minute introductory call? I am available Monday through Wednesday of next week. Please let me know what day and time works best for your schedule.\n\nLooking forward to speaking soon.\n\nBest regards,\n\n[My Name]"
    },
    {
        "id": 2,
        "intent": "Follow up on a job application submitted 2 weeks ago",
        "facts": ["Applied for Senior Data Analyst role", "Application submitted on June 1st", "Have not heard back", "Attached portfolio link in original application"],
        "tone": "Polite and persistent",
        "human_reference": "Subject: Checking in - Senior Data Analyst Application (June 1st)\n\nHi [Hiring Manager Name],\n\nI hope this email finds you well.\n\nI submitted my application for the Senior Data Analyst position on June 1st and wanted to quickly follow up. I'm very excited about the opportunity to bring my data expertise to your team.\n\nAs a reminder, I included a link to my portfolio in my original application so you can review some of my recent work.\n\nPlease let me know if you need any additional information from me or have an update regarding the timeline. Thank you for your time and consideration.\n\nBest,\n\n[My Name]"
    },
    {
        "id": 3,
        "intent": "Apologize for missing a deadline",
        "facts": ["Report was due on Friday", "Missed due to unexpected server outage", "New delivery date: Tuesday EOD", "Will add executive summary as compensation"],
        "tone": "Apologetic and accountable",
        "human_reference": "Subject: Update on [Project Name] Report Delivery\n\nHi [Name],\n\nI want to sincerely apologize for missing our Friday deadline on the report. We experienced an unexpected server outage that temporarily blocked access to critical data needed to complete the analysis.\n\nI completely own this delay. To make up for it, I am putting together an additional executive summary that highlights the key findings upfront to save you time. \n\nYou will have the full report along with the executive summary by Tuesday EOD at the latest.\n\nThank you for your patience and understanding.\n\nBest regards,\n\n[My Name]"
    },
    {
        "id": 4,
        "intent": "Send a project status update to stakeholders",
        "facts": ["Phase 1 complete: data migration done", "Phase 2 on track, 70% complete", "Risk: third-party API delay may push timeline by 3 days", "Next review: July 15th"],
        "tone": "Formal and informative",
        "human_reference": "Subject: Project Status Update - [Project Name]\n\nDear Stakeholders,\n\nI am writing to provide our latest project status update. I'm pleased to report that Phase 1 is fully complete, and we have successfully finished the data migration.\n\nWe are currently progressing through Phase 2, which is 70% complete and generally on track. However, there is a minor risk we are monitoring: a delay from a third-party API integration may push our final timeline out by roughly three days.\n\nWe will continue to navigate the API delay and report back. Our next scheduled status review is set for July 15th.\n\nBest regards,\n\n[My Name]"
    },
    {
        "id": 5,
        "intent": "Negotiate a contract renewal with a vendor",
        "facts": ["Current contract ends August 31st", "Want 15% price reduction", "Competitor quote is 20% lower", "Willing to sign 2-year deal in exchange for discount"],
        "tone": "Firm but collaborative",
        "human_reference": "Subject: Contract Renewal Discussion\n\nHi [Vendor Name],\n\nI’m reaching out because our current contract is set to expire on August 31st. We have appreciated your partnership over this past term and would ideally like to continue working together.\n\nAs we plan our budget for next year, we are looking for a 15% price reduction on the renewal. To be fully transparent, we recently received a competitor quote that is 20% lower than our current rate. That said, because we value our existing relationship, we are more than willing to commit to a 2-year agreement in exchange for the 15% discount.\n\nPlease let me know when you are free to discuss this further.\n\nBest regards,\n\n[My Name]"
    },
    {
        "id": 6,
        "intent": "Invite team to a company offsite event",
        "facts": ["Date: August 10-11", "Location: Coorg, Karnataka", "Activities: team workshops + hiking", "RSVP required by July 25th", "Travel and stay fully covered"],
        "tone": "Enthusiastic and casual",
        "human_reference": "Subject: 🎉 Pack your bags! Our Team Offsite in Coorg\n\nHey team!\n\nI am thrilled to announce our upcoming company offsite! We are heading out on August 10-11 for an amazing trip to Coorg, Karnataka.\n\nWe’ve got a fantastic schedule planned that blends some team-building workshops with a fun hiking adventure. Don't worry about the logistics—all your travel and stay expenses are fully covered by the company.\n\nPlease RSVP by July 25th so we can finalize the bookings.\n\nCan’t wait to celebrate all our hard work together!\n\nCheers,\n\n[My Name]"
    },
    {
        "id": 7,
        "intent": "Reject a candidate after an interview",
        "facts": ["Candidate interviewed for Product Manager role", "Strong technical background", "Team felt communication skills were not at the required level", "Encourage reapplying in 6 months"],
        "tone": "Empathetic and respectful",
        "human_reference": "Subject: Update on the Product Manager Application\n\nDear [Candidate Name],\n\nThank you for taking the time to interview with us for the Product Manager role. We truly enjoyed speaking with you and getting to know more about your experience.\n\nWhile the team was very impressed with your strong technical background, we have decided to move forward with a candidate whose communication skills more closely align with the specific cross-functional needs of this role right now.\n\nWe genuinely appreciate your interest in our company. We encourage you to keep an eye on our careers page and re-apply in about 6 months as new opportunities open up.\n\nWishing you all the best in your career journey.\n\nBest regards,\n\n[My Name]\n[Company Name]"
    },
    {
        "id": 8,
        "intent": "Request urgent approval for a budget increase",
        "facts": ["Original budget: ₹5,00,000", "Revised estimate: ₹6,80,000", "Reason: raw material cost surge of 36%", "Project halt risk if not approved by Friday"],
        "tone": "Urgent and factual",
        "human_reference": "Subject: URGENT: Budget Increase Request for [Project Name]\n\nHi [Manager Name],\n\nI am writing to formally request an urgent approval for a budget increase on [Project Name].\n\nOur original budget was set at ₹5,00,000. However, due to a recent, unexpected 36% surge in raw material costs, our new revised estimate to complete the work is ₹6,80,000.\n\nWithout this approval, we risk a complete halt to the project. I need your sign-off by this Friday to keep the timeline on track.\n\nPlease let me know if you need to review the cost breakdown immediately.\n\nBest,\n\n[My Name]"
    },
    {
        "id": 9,
        "intent": "Thank a mentor after career advice",
        "facts": ["Mentor helped navigate a difficult career pivot", "Advice led to accepting a new role at a fintech startup", "Starting date is next Monday", "Plan to stay in touch quarterly"],
        "tone": "Warm and genuine",
        "human_reference": "Subject: Thank you for the incredible guidance so far!\n\nHi [Mentor Name],\n\nI am reaching out to give you a massive thank you. Your advice over these past few months helped me immensely in navigating what felt like a very difficult career pivot.\n\nThanks to your guidance, I am thrilled to share that I have officially accepted a new role at a fintech startup! I will be starting next Monday, and I couldn't have made this leap without your candid feedback.\n\nI would love to keep you updated on my journey and plan to stay in touch quarterly, if that works for you.\n\nThank you again for your time and mentorship.\n\nBest,\n\n[My Name]"
    },
    {
        "id": 10,
        "intent": "Onboard a new client to a SaaS platform",
        "facts": ["Client: Meridian Retail Ltd", "Onboarding call scheduled for July 8th, 3 PM IST", "Login credentials sent separately", "Dedicated support: Priya Sharma, priya@company.com", "Help docs: docs.company.com"],
        "tone": "Friendly and professional",
        "human_reference": "Subject: Welcome to [Platform Name] - Next Steps\n\nHi Meridian Retail Ltd Team,\n\nWelcome! We are incredibly excited to have you onboard.\n\nTo get everything rolling, we have your kickoff onboarding call scheduled for July 8th at 3 PM IST. Prior to that call, you will receive a separate automated email containing your secure login credentials.\n\nIf you have any questions along the way, Priya Sharma will be your dedicated support contact and can be reached directly at priya@company.com. You can also explore our help documentation at docs.company.com at any time.\n\nWe look forward to speaking with you on the 8th!\n\nBest regards,\n\n[My Name]\n[Company Name]"
    }
]
