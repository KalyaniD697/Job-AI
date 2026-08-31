import { useState } from "react";


function SearchForm({ onSearch, loading }) {

    const [role, setRole] = useState(
        "Python Developer"
    );

    const [location, setLocation] = useState(
        "Hyderabad"
    );

    const [experience, setExperience] = useState(
        "0-2 years"
    );


    const handleSubmit = (event) => {

        event.preventDefault();

        if (!role.trim()) {
            alert("Please enter a job role");
            return;
        }

        if (!location.trim()) {
            alert("Please enter a location");
            return;
        }

        if (!experience.trim()) {
            alert("Please enter experience");
            return;
        }

        onSearch({
            role: role.trim(),
            location: location.trim(),
            experience: experience.trim(),
        });
    };


    return (
        <form
            className="search-form"
            onSubmit={handleSubmit}
        >

            <div className="form-group">

                <label htmlFor="role">
                    Job Role
                </label>

                <input
                    id="role"
                    type="text"
                    value={role}
                    onChange={(event) =>
                        setRole(event.target.value)
                    }
                    placeholder="e.g. Python Developer"
                />

            </div>


            <div className="form-group">

                <label htmlFor="location">
                    Location
                </label>

                <input
                    id="location"
                    type="text"
                    value={location}
                    onChange={(event) =>
                        setLocation(event.target.value)
                    }
                    placeholder="e.g. Hyderabad"
                />

            </div>


            <div className="form-group">

                <label htmlFor="experience">
                    Experience
                </label>

                <input
                    id="experience"
                    type="text"
                    value={experience}
                    onChange={(event) =>
                        setExperience(event.target.value)
                    }
                    placeholder="e.g. 0-2 years"
                />

            </div>


            <button
                type="submit"
                disabled={loading}
            >
                {loading
                    ? "Searching..."
                    : "🔍 Search Jobs"
                }
            </button>

        </form>
    );
}


export default SearchForm;