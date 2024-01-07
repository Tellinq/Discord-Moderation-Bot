import disnake
from disnake.ext import plugins, commands


plugin = plugins.Plugin()


@plugin.slash_command()
async def info(inter: disnake.GuildCommandInteraction):
    """Command group related to fetching info"""
    pass


@info.sub_command()
async def bot(inter: disnake.GuildCommandInteraction):
    """Get details about the bot"""
    embed = disnake.Embed(title=plugin.bot.user.name)
    embed.set_thumbnail(plugin.bot.user.display_avatar)
    
    embed.add_field("Latency", f"{round(plugin.bot.latency * 1000)}ms", inline=False)
    embed.add_field("Servers Joined", len(plugin.bot.guilds), inline=False)
    embed.add_field("Commands", len(plugin.bot.slash_commands), inline=False)

    await inter.send(embed=embed)


@info.sub_command()
async def user(inter: disnake.GuildCommandInteraction, target: disnake.User = commands.Param(lambda inter: inter.author)):
    """
    Get details about a user/member

    Parameters
    ----------
    target: The user/member to get details of
    """
    # format the username based on if they are still using discrims or not
    username = f"@{target}" if target.discriminator == "0" else target
    
    embed = disnake.Embed(title=username)
    embed.set_footer(text=f"ID: {target.id}")
    embed.set_thumbnail(target.display_avatar)
    
    embed.add_field(
        "Created",
        disnake.utils.format_dt(target.created_at, "R"),
        inline=False
    )
    
    if isinstance(target, disnake.Member):
        if target.joined_at:
            join_date = disnake.utils.format_dt(target.joined_at, "R")
        else:
            join_date = "unavailable"

        embed.add_field(
            "Joined",
            join_date,
            inline=False
        )
        
        roles = target.roles[1:] # exclude @everyone
        
        if roles:
            embed.add_field(
                f"Roles [{len(roles)}]",
                ", ".join(role.mention for role in roles),
                inline=False
            )
        
    await inter.send(embed=embed)
    
    
@info.sub_command()
async def server(inter: disnake.GuildCommandInteraction):
    """Get details about the server"""
    embed = disnake.Embed(
        title=inter.guild.name,
        description=inter.guild.description
    )
    
    embed.set_thumbnail(inter.guild.icon)
    
    embed.add_field(
        "Owner",
        inter.guild.owner.mention if inter.guild.owner is not None else "unknown",
        inline=False
    )
    
    embed.add_field(
        "Created",
        disnake.utils.format_dt(inter.guild.created_at, "R"),
        inline=False
    )
    
    embed.add_field(
        "Members",
        inter.guild.member_count,
        inline=False
    )
    
    await inter.send(embed=embed)
    

setup, teardown = plugin.create_extension_handlers()