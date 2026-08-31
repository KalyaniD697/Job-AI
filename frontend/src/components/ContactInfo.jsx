function ContactInfo({
    contact,
    job,
    onGenerateEmail,
}) {

    if (!contact) {
        return null;
    }


    return (
        <div className="contact-panel">

            <div className="panel-header">

                <div>

                    <h2>
                        Contact Information
                    </h2>

                    <p>
                        {job.company ||
                            "Company"}
                    </p>

                </div>

                <span className="confidence">
                    {Math.round(
                        (contact.confidence || 0) * 100
                    )}% confidence
                </span>

            </div>


            <div className="contact-details">

                {contact.contact_name && (

                    <div className="contact-item">

                        <strong>
                            Contact
                        </strong>

                        <span>
                            {contact.contact_name}
                        </span>

                    </div>

                )}


                {contact.contact_email ? (

                    <div className="contact-item">

                        <strong>
                            Email
                        </strong>

                        <a
                            href={`mailto:${contact.contact_email}`}
                        >
                            {contact.contact_email}
                        </a>

                    </div>

                ) : (

                    <div className="contact-item">

                        <strong>
                            Email
                        </strong>

                        <span>
                            No public email found
                        </span>

                    </div>

                )}


                {contact.linkedin_url && (

                    <div className="contact-item">

                        <strong>
                            LinkedIn
                        </strong>

                        <a
                            href={contact.linkedin_url}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            View LinkedIn ↗
                        </a>

                    </div>

                )}


                {contact.company_website && (

                    <div className="contact-item">

                        <strong>
                            Website
                        </strong>

                        <a
                            href={contact.company_website}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Visit Website ↗
                        </a>

                    </div>

                )}

            </div>


            <button
                className="primary-button"
                onClick={() =>
                    onGenerateEmail(job)
                }
            >
                ✉ Generate Application Email
            </button>

        </div>
    );
}


export default ContactInfo;