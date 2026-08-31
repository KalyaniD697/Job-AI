const API_BASE_URL = "http://127.0.0.1:8000/api/jobs";


export async function searchJobs(
    role,
    location,
    experience
) {
    const response = await fetch(
        `${API_BASE_URL}/search/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                role,
                location,
                experience,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "Failed to search jobs"
        );
    }

    return data;
}


export async function findContact(
    company,
    jobTitle,
    location
) {
    const response = await fetch(
        `${API_BASE_URL}/contact/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                company,
                job_title: jobTitle,
                location,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "Failed to find contact"
        );
    }

    return data;
}


export async function generateEmail(
    job,
    candidate
) {
    const response = await fetch(
        `${API_BASE_URL}/generate-email/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                job,
                candidate,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "Failed to generate email"
        );
    }

    return data;
}