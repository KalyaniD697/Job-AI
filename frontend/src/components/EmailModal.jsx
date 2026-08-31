function EmailModal({
    email,
    contact,
    onClose,
}) {

    if (!email) {
        return null;
    }


    const copyEmail = async () => {

        const emailText =
            `Subject: ${email.subject}\n\n${email.body}`;

        try {

            await navigator.clipboard.writeText(
                emailText
            );

            alert(
                "Email copied to clipboard!"
            );

        } catch (error) {

            console.error(error);

            alert(
                "Unable to copy email"
            );
        }
    };


    return (
        <div
            className="modal-overlay"
            onClick={onClose}
        >

            <div
                className="email-modal"
                onClick={(event) =>
                    event.stopPropagation()
                }
            >

                <button
                    className="close-button"
                    onClick={onClose}
                    aria-label="Close"
                >
                    ✕
                </button>


                <h2>
                    Application Email
                </h2>


                {contact?.contact_email && (

                    <div className="email-to">

                        <strong>
                            To:
                        </strong>{" "}

                        {contact.contact_email}

                    </div>

                )}


                <label>
                    Subject
                </label>

                <input
                    value={email.subject}
                    readOnly
                />


                <label>
                    Email Body
                </label>

                <textarea
                    value={email.body}
                    readOnly
                    rows={14}
                />


                <div className="email-actions">

                    <button
                        className="primary-button"
                        onClick={copyEmail}
                    >
                        📋 Copy Email
                    </button>

                    <button
                        className="secondary-button"
                        onClick={onClose}
                    >
                        Close
                    </button>

                </div>

            </div>

        </div>
    );
}


export default EmailModal;