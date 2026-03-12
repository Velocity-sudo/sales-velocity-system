import { notion } from '../../../../src/lib/notion';
import { config } from '../../../../src/config';
import { withRetry } from '../../../../src/lib/retry';

async function main() {
    console.log("🔍 Starting Notion Health Check...");

    // 1. Verify Environment Variables
    console.log("Checking configuration...");
    const requiredVars = [
        'NOTION_API_KEY',
        'NOTION_DATABASE_ID_CLIENTS',
        'NOTION_DATABASE_ID_DELIVERABLES'
    ];

    const missing = requiredVars.filter(v => !process.env[v]);
    if (missing.length > 0) {
        console.error(`❌ Missing environment variables: ${missing.join(', ')}`);
        process.exit(1);
    }
    console.log("✅ Configuration present.");

    // 2. Test Connection (Get User)
    console.log("\nTesting API Connection...");
    try {
        const user = await withRetry(() => notion.users.me({}));
        console.log(`✅ Connected as bot: ${user.name || 'Unknown'} (${user.type})`);
    } catch (error: any) {
        console.error(`❌ Connection failed: ${error.message}`);
        if (error.status === 401) {
            console.error("   -> Check if NOTION_API_KEY is correct.");
        }
        process.exit(1);
    }

    // 3. Test Database Access (Clients)
    console.log("\nTesting 'Clients' Database Access...");
    try {
        await withRetry(() => notion.databases.retrieve({ database_id: config.NOTION_DATABASE_ID_CLIENTS }));
        console.log("✅ 'Clients' database is accessible.");
    } catch (error: any) {
        console.error(`❌ Failed to access 'Clients' database: ${error.message}`);
        if (error.status === 404) {
            console.error("   -> Ensure the ID is correct and the bot is invited to this database.");
        }
    }

    // 4. Test Database Access (Deliverables)
    console.log("\nTesting 'Deliverables' Database Access...");
    try {
        await withRetry(() => notion.databases.retrieve({ database_id: config.NOTION_DATABASE_ID_DELIVERABLES }));
        console.log("✅ 'Deliverables' database is accessible.");
    } catch (error: any) {
        console.error(`❌ Failed to access 'Deliverables' database: ${error.message}`);
        if (error.status === 404) {
            console.error("   -> Ensure the ID is correct and the bot is invited to this database.");
        }
    }

    console.log("\n----- Health Check Complete -----");
}

main().catch(console.error);
