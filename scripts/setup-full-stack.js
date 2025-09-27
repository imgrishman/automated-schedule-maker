const { spawn, exec } = require("child_process")
const fs = require("fs")
const path = require("path")

console.log("🚀 AUTOMATED SCHEDULE PLANNER - FULL STACK SETUP")
console.log("=" * 60)

async function runCommand(command, cwd = process.cwd()) {
  return new Promise((resolve, reject) => {
    console.log(`🔧 Running: ${command}`)
    exec(command, { cwd }, (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Error: ${error.message}`)
        reject(error)
        return
      }
      if (stderr) {
        console.log(`⚠️ Warning: ${stderr}`)
      }
      console.log(`✅ Success: ${command}`)
      resolve(stdout)
    })
  })
}

async function setupFullStack() {
  try {
    console.log("\n📦 STEP 1: Setting up Frontend Dependencies")
    console.log("-".repeat(50))

    // Install frontend dependencies
    await runCommand("npm install")

    console.log("\n🐍 STEP 2: Setting up Backend")
    console.log("-".repeat(50))

    // Setup backend
    await runCommand("python scripts/install_dependencies.py", "./backend")
    await runCommand("python scripts/setup_database_sync.py", "./backend")

    console.log("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
    console.log("=" * 60)
    console.log("🔗 Frontend: http://localhost:3000")
    console.log("🔗 Backend API: http://localhost:8000")
    console.log("📖 API Docs: http://localhost:8000/docs")

    console.log("\n🔐 Demo Credentials:")
    console.log("👑 Admin: admin@asp.com / admin123")
    console.log("👨‍💼 Manager: manager@asp.com / manager123")
    console.log("👤 Employee: demo@asp.com / demo123")

    console.log("\n🚀 To start the application:")
    console.log("1. Backend: cd backend && python main.py")
    console.log("2. Frontend: npm run dev")

    // Ask if user wants to start servers
    const readline = require("readline")
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    })

    rl.question("\n❓ Start both servers now? (y/n): ", (answer) => {
      if (answer.toLowerCase() === "y" || answer.toLowerCase() === "yes") {
        console.log("\n🚀 Starting servers...")

        // Start backend
        const backend = spawn("python", ["main.py"], {
          cwd: "./backend",
          stdio: "inherit",
        })

        // Start frontend after a delay
        setTimeout(() => {
          const frontend = spawn("npm", ["run", "dev"], {
            stdio: "inherit",
          })
        }, 3000)

        console.log("✅ Servers starting...")
        console.log("🌐 Frontend will be available at: http://localhost:3000")
        console.log("🔧 Backend API available at: http://localhost:8000")
        console.log("🛑 Press Ctrl+C to stop servers")
      } else {
        console.log("\n👋 Setup completed! Start servers manually when ready.")
      }
      rl.close()
    })
  } catch (error) {
    console.error("❌ Setup failed:", error.message)
    process.exit(1)
  }
}

setupFullStack()
