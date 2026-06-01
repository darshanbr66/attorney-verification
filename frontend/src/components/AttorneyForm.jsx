
// frontend/src/components/AttorneyForm.jsx
import { useState } from "react";

const AttorneyForm = ({
  onSubmit,
  loading,
}) => {

  const [form, setForm] = useState({
    name: "",
    reg_no: "",
    organization: "",
    city: "",
  });

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]:
        e.target.value,
    });

  };

  const clearForm = () => {

    setForm({
      name: "",
      reg_no: "",
      organization: "",
      city: "",
    });

  };

  return (
    <div
      className="
        bg-white/[0.03]
        border
        border-white/10
        rounded-3xl
        backdrop-blur-xl
        p-8
      "
    >

      <div className="space-y-5">

        <input
          type="text"
          name="name"
          placeholder="Attorney Name *"
          value={form.name}
          onChange={handleChange}
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            bg-[#0B1120]
            border
            border-white/10
            outline-none
          "
        />

        <input
          type="text"
          name="reg_no"
          placeholder="Registration Number"
          value={form.reg_no}
          onChange={handleChange}
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            bg-[#0B1120]
            border
            border-white/10
            outline-none
          "
        />

        <input
          type="text"
          name="organization"
          placeholder="Organization"
          value={form.organization}
          onChange={handleChange}
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            bg-[#0B1120]
            border
            border-white/10
            outline-none
          "
        />

        <input
          type="text"
          name="city"
          placeholder="City (Optional)"
          value={form.city}
          onChange={handleChange}
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            bg-[#0B1120]
            border
            border-white/10
            outline-none
          "
        />

        <div
          className="
            flex
            gap-4
            flex-wrap
          "
        >

          <button
            onClick={() =>
              onSubmit(form)
            }
            disabled={loading}
            className="
              px-8
              py-4
              rounded-2xl
              bg-cyan-400
              text-black
              font-semibold
              hover:bg-cyan-300
              transition
            "
          >
            Verify Attorney
          </button>

          <button
            onClick={clearForm}
            type="button"
            className="
              px-8
              py-4
              rounded-2xl
              border
              border-white/10
              bg-white/[0.04]
              text-white
            "
          >
            Clear Form
          </button>

        </div>

      </div>

    </div>
  );
};

export default AttorneyForm;