import { useState } from "react";

import SearchForm from "./components/SearchForm";
import JobCard from "./components/JobCard";
import ContactInfo from "./components/ContactInfo";
import EmailModal from "./components/EmailModal";

import {
    searchJobs,
    findContact,
    generateEmail,
} from "./services/api";

import "./App.css";


function App() {

    const [jobs, setJobs] = useState([]);

    const [loading, setLoading] =
        useState(false);

    const [contactLoading, setContactLoading] =
        useState(false);

    const [emailLoading, setEmailLoading] =
        useState(false);

    const [selectedJob, setSelectedJob] =
        useState(null);

    const [contact, setContact] =
        useState(null);

    const [email, setEmail] =
        useState(null);

    const [error, setError] =
        useState("");


    const handleSearch = async (filters) => {

        try {

            setLoading(true);

            setError("");

            setJobs([]);

            setContact(null);

            setSelectedJob(null);

            const data = await searchJobs(
                filters.role,
                filters.location,
                filters.experience
            );

            setJobs(
                data.jobs || []
            );

        } catch (error) {

            console.error(error);

            setError(
                error.message ||
                "Failed to search jobs"
            );

        } finally {

            setLoading(false);
        }
    };


    const handleFindContact = async (job) => {

        try {

            setContactLoading(true);

            setError("");

            setSelectedJob(job);

            setContact(null);

            const data =
                await findContact(
                    job.company,
                    job.title,
                    job.location
                );

            setContact(
                data.contact
            );

        } catch (error) {

            console.error(error);

            setError(
                error.message ||
                "Failed to find contact"
            );

        } finally {

            setContactLoading(false);
        }
    };


    const handleGenerateEmail = async (job) => {

        try {

            setEmailLoading(true);

            setError("");

            const candidate = {

                name: "Your Name",

                skills: [
                    "Python",
                    "Django",
                    "Django REST Framework",
                    "SQL",
                    "React",
                ],

                experience: "0-2 years",

                projects: [
                    "GenAI PDF Q&A application",
                ],
            };


            const data =
                await generateEmail(
                    job,
                    candidate
                );


            setEmail(
                data.email
            );

        } catch (error) {

            console.error(error);

            setError(
                error.message ||
                "Failed to generate email"
            );

        } finally {

            setEmailLoading(false);
        }
    };


    return (

        <div className="app">

            <header className="app-header">

                <div className="header-content">

                    <div className="logo">
                        🤖
                    </div>

                    <div>

                        <h1>
                            Job AI
                        </h1>

                        <p>
                            AI-Powered Job Search Assistant
                        </p>

                    </div>

                </div>

            </header>


            <main className="container">

                <section className="search-section">

                    <div className="section-title">

                        <h2>
                            Find Your Next Job
                        </h2>

                        <p>
                            Search relevant jobs and
                            discover public contact
                            information.
                        </p>

                    </div>


                    <SearchForm
                        onSearch={handleSearch}
                        loading={loading}
                    />

                </section>


                {error && (

                    <div className="error-message">

                        ⚠️ {error}

                    </div>

                )}


                {loading && (

                    <div className="loading">

                        <div className="spinner"></div>

                        <p>
                            Searching for relevant jobs...
                        </p>

                    </div>

                )}


                {!loading &&
                    jobs.length > 0 && (

                    <section className="results-section">

                        <div className="results-header">

                            <h2>
                                Job Results
                            </h2>

                            <span>
                                {jobs.length} jobs found
                            </span>

                        </div>


                        <div className="jobs-list">

                            {jobs.map(
                                (job, index) => (

                                    <JobCard
                                        key={
                                            job.job_url ||
                                            index
                                        }
                                        job={job}
                                        onFindContact={
                                            handleFindContact
                                        }
                                        onGenerateEmail={
                                            handleGenerateEmail
                                        }
                                    />

                                )
                            )}

                        </div>

                    </section>

                )}


                {!loading &&
                    jobs.length === 0 &&
                    !error && (

                    <div className="empty-state">

                        <div>
                            🔎
                        </div>

                        <h2>
                            Search for jobs
                        </h2>

                        <p>
                            Enter a role, location and
                            experience level above to
                            discover relevant opportunities.
                        </p>

                    </div>

                )}


                {contactLoading && (

                    <div className="loading-overlay">

                        <div className="loading-card">

                            <div className="spinner"></div>

                            <h3>
                                Finding Contact
                            </h3>

                            <p>
                                Searching public company
                                sources...
                            </p>

                        </div>

                    </div>

                )}


                {contact && selectedJob && (

                    <ContactInfo
                        contact={contact}
                        job={selectedJob}
                        onGenerateEmail={
                            handleGenerateEmail
                        }
                    />

                )}


                {emailLoading && (

                    <div className="loading-overlay">

                        <div className="loading-card">

                            <div className="spinner"></div>

                            <h3>
                                Creating Email
                            </h3>

                            <p>
                                Personalizing your
                                application...
                            </p>

                        </div>

                    </div>

                )}

            </main>


            {email && (

                <EmailModal
                    email={email}
                    contact={contact}
                    onClose={() =>
                        setEmail(null)
                    }
                />

            )}

        </div>
    );
}


export default App;