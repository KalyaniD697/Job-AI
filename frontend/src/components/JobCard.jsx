function JobCard({
    job,
    onFindContact,
    onGenerateEmail,
}) {

    const matchPercentage =
        job.match_score !== undefined
            ? Math.round(job.match_score * 100)
            : null;


    return (
        <article className="job-card">

            <div className="job-header">

                <div>

                    <h3>
                        {job.title}
                    </h3>

                    <p className="company">
                        {job.company ||
                            "Company not available"}
                    </p>

                </div>

                {matchPercentage !== null && (

                    <div className="match-score">
                        {matchPercentage}% Match
                    </div>

                )}

            </div>


            <div className="job-meta">

                {job.location && (
                    <span>
                        📍 {job.location}
                    </span>
                )}

                {job.experience && (
                    <span>
                        💼 {job.experience}
                    </span>
                )}

            </div>


            {job.skills &&
                job.skills.length > 0 && (

                <div className="skills">

                    {job.skills.map(
                        (skill, index) => (

                            <span
                                className="skill"
                                key={index}
                            >
                                {skill}
                            </span>

                        )
                    )}

                </div>

            )}


            {job.description && (

                <p className="description">
                    {job.description}
                </p>

            )}


            {job.match_reason && (

                <p className="match-reason">
                    <strong>
                        Why it matches:
                    </strong>{" "}
                    {job.match_reason}
                </p>

            )}


            <div className="job-actions">

                {job.job_url && (

                    <a
                        href={job.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="secondary-button"
                    >
                        View Job ↗
                    </a>

                )}


                <button
                    className="secondary-button"
                    onClick={() =>
                        onFindContact(job)
                    }
                >
                    Find Contact
                </button>


                <button
                    className="primary-button"
                    onClick={() =>
                        onGenerateEmail(job)
                    }
                >
                    ✉ Generate Email
                </button>

            </div>

        </article>
    );
}


export default JobCard;